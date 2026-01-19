"""
Excel XML Reader Adapter
-------------------------
Reads Excel 2003 XML format files and converts them to pandas DataFrame.
Handles special characters properly to match XLSX output exactly.
"""

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import html
import re

import pandas as pd

logger = logging.getLogger(__name__)

# XML namespaces used in Excel 2003 XML format
NAMESPACES = {
    'ss': 'urn:schemas-microsoft-com:office:spreadsheet',
    'o': 'urn:schemas-microsoft-com:office:office',
    'x': 'urn:schemas-microsoft-com:office:excel',
    'html': 'http://www.w3.org/TR/REC-html40'
}


class ExcelXMLReader:
    """
    Reader for Excel 2003 XML format (.xml files exported from Celer).
    
    Handles the SpreadsheetML format which uses nested XML structure
    with Workbook > Worksheet > Table > Row > Cell elements.
    Properly preserves special characters like &, accents, etc.
    """
    
    def __init__(self):
        self.namespaces = NAMESPACES
        logger.info("ExcelXMLReader initialized")
    
    def _preprocess_xml(self, file_path: Path) -> bytes:
        """
        Pre-process XML file to handle special characters properly.
        Reads the file and ensures entities are properly encoded.
        
        Args:
            file_path: Path to XML file
            
        Returns:
            Processed XML content as bytes
        """
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Fix common entity issues in malformed XML
        # Excel XML should have entities properly encoded, but Celer might not
        # We need to be careful not to break existing proper XML
        # Only fix entities within Data elements
        def fix_data_content(match):
            """Fix entities in Data element content"""
            opening = match.group(1)
            content_text = match.group(2)
            closing = match.group(3)
            
            # Replace special characters with entities
            fixed_content = content_text
            fixed_content = fixed_content.replace('&', '&amp;')
            fixed_content = fixed_content.replace('&amp;amp;', '&amp;')
            
            return opening + fixed_content + closing
        
        # Pattern to match Data elements with content
        # This preserves XML structure while fixing content
        pattern = r'(<Data[^>]*>)(.*?)(</Data>)'
        content = re.sub(pattern, fix_data_content, content, flags=re.DOTALL)
        
        return content.encode('utf-8')
    
    def read_xml_to_dataframe(
        self, 
        file_path: Path, 
        header_row: int = 4
    ) -> pd.DataFrame:
        """
        Read Excel XML file and convert to pandas DataFrame.
        Uses lxml parser with special character preservation.
        
        Args:
            file_path: Path to XML file
            header_row: Row index where headers are located (0-indexed)
            
        Returns:
            DataFrame with data from XML file
        """
        logger.info(f"Reading XML file: {file_path}")
        
        # Pre-process the XML file to fix common entity issues
        xml_content = self._preprocess_xml(file_path)
        
        try:
            # Try with lxml parser (more robust)
            try:
                import lxml.etree as letree
                parser = letree.XMLParser(recover=True, encoding='utf-8')
                root = letree.fromstring(xml_content, parser)
                logger.info("Successfully parsed XML with lxml (recover mode)")
            except ImportError:
                # Fallback to built-in ElementTree
                logger.warning("lxml not available, using built-in ElementTree")
                root = ET.fromstring(xml_content)
            
        except Exception as e:
            logger.error(f"Failed to parse XML file: {e}")
            raise ValueError(f"Failed to parse XML file: {e}")
        
        # Find the worksheet (usually first one)
        worksheet = root.find('.//ss:Worksheet', self.namespaces)
        if worksheet is None:
            raise ValueError("No Worksheet found in XML file")
        
        # Find the table
        table = worksheet.find('.//ss:Table', self.namespaces)
        if table is None:
            raise ValueError("No Table found in Worksheet")
        
        # Extract all rows
        rows = table.findall('.//ss:Row', self.namespaces)
        logger.info(f"Found {len(rows)} rows in XML")
        
        # Parse rows into list of lists
        data_rows = []
        headers = None
        
        for row_idx, row in enumerate(rows):
            row_data = self._parse_row(row)
            
            if row_idx == header_row:
                # This is the header row
                headers = row_data
                logger.info(f"Found {len(headers)} headers at row {header_row}")
            elif row_idx > header_row:
                # Data rows after header
                data_rows.append(row_data)
        
        if headers is None:
            raise ValueError(f"No header row found at index {header_row}")
        
        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        
        logger.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def _parse_row(self, row_element: ET.Element) -> List[Any]:
        """
        Parse a Row element into a list of cell values.
        
        Args:
            row_element: XML Element representing a Row
            
        Returns:
            List of cell values
        """
        cells = row_element.findall('.//ss:Cell', self.namespaces)
        row_data = []
        current_index = 0
        
        for cell in cells:
            # Check if cell has an Index attribute (indicates sparse columns)
            index_attr = cell.get(f'{{{self.namespaces["ss"]}}}Index')
            
            if index_attr:
                # Cell specifies its position, fill gaps with None
                target_index = int(index_attr) - 1  # Convert to 0-based
                while current_index < target_index:
                    row_data.append(None)
                    current_index += 1
            
            # Extract cell value
            data_element = cell.find('.//ss:Data', self.namespaces)
            
            if data_element is not None and data_element.text:
                # Get data type
                data_type = data_element.get(f'{{{self.namespaces["ss"]}}}Type', 'String')
                
                # Parse value based on type
                value = self._parse_cell_value(data_element.text, data_type)
                row_data.append(value)
            else:
                row_data.append(None)
            
            current_index += 1
        
        return row_data
    
    def _parse_cell_value(self, text: str, data_type: str) -> Any:
        """
        Parse cell value based on its type.
        Properly decodes HTML/XML entities to preserve special characters.
        
        Args:
            text: Cell text content
            data_type: Data type (String, Number, DateTime, etc.)
            
        Returns:
            Parsed value with special characters preserved
        """
        if text is None or text.strip() == '':
            return None
        
        # Decode HTML entities (like &amp; -> &)
        text = html.unescape(text)
        
        # Clean text (remove extra whitespace, newlines)
        text = ' '.join(text.split())
        
        if data_type == 'Number':
            try:
                # Try integer first
                if '.' not in text:
                    return int(text)
                return float(text)
            except ValueError:
                return text
        
        elif data_type == 'DateTime':
            # Keep as string, pandas will handle date parsing
            return text
        
        # Default: return as string with special characters preserved
        return text


def read_celer_xml(file_path: Path, header_row: int = 4) -> pd.DataFrame:
    """
    Convenience function to read Celer XML export.
    
    Args:
        file_path: Path to Celer XML file
        header_row: Row index where headers are (default: 4 for Celer exports)
        
    Returns:
        DataFrame with Celer data
    """
    reader = ExcelXMLReader()
    return reader.read_xml_to_dataframe(file_path, header_row)
