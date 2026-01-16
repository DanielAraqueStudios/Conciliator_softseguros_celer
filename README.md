# Conciliator SoftSeguros Celer

**Production-Grade Python Backend for Excel Automation**

A robust Python application designed to ingest, transform, validate, and export insurance data to/from Excel (XLSX) with high reliability and performance.

---

## 🎯 Project Mission

Build and maintain a production-ready backend that:
- ✅ Ingests, transforms, validates, and exports data to/from Excel reliably
- ✅ Generates polished Excel reports/templates (tables, formulas, styles, charts)
- ✅ Integrates with databases and APIs as needed
- ✅ Is production-grade: testable, secure, maintainable, and performant

**This is not a toy script. This is deployable, maintainable code.**

---

## 🏗️ Architecture

```
conciliator_softseguros_celer/
├── domain/             # Business rules and models
├── services/           # Orchestration and workflows
├── adapters/           # Excel IO, DB IO, external API clients
├── schemas/            # Pydantic models and validation rules
├── tests/              # Unit and integration tests
├── config/             # Configuration management
├── logs/               # Application logs
└── output/             # Generated Excel files
```

---

## 🔧 Technical Stack

### Core Libraries
- **Python 3.x** with comprehensive type hints (mypy-compatible)
- **openpyxl**: Excel read/write operations with styling support
- **pandas**: Data transformation and analysis
- **pydantic**: Data validation and schema enforcement
- **sqlalchemy**: Database access (if needed)
- **fastapi**: REST API endpoints (if needed)

### Development Tools
- **pytest**: Testing framework
- **mypy**: Static type checking
- **ruff/black**: Code formatting
- **pre-commit**: Git hooks for quality checks

---

## 📋 Technical Priorities

### 1. **Correctness Over Cleverness**
- Data integrity, validation, and reproducibility are mandatory
- No shortcuts that compromise data quality

### 2. **Excel Output Must Be Deterministic**
- Same input → same file structure, styles, sheet names, and ordering
- Consistent across different OS/timezone/locale environments

### 3. **Performance for Large Files**
- Streaming or chunking when possible
- Avoid O(n²) loops; use vectorization
- Bulk operations preferred over cell-by-cell

### 4. **Observability**
- Structured logging with correlation IDs
- Meaningful error messages
- Clear exception boundaries

### 5. **Security**
- Never eval Excel content or execute untrusted macros
- Sanitize file paths
- Validate all input schemas

---

## 📊 Excel-Specific Standards

### Reading Excel Files
**Validation Requirements:**
- ✅ Required sheets exist
- ✅ Headers match expected schema
- ✅ Data types and constraints (dates, numeric ranges, enums)

**Edge Cases Handled:**
- Merged cells
- Empty rows
- Hidden sheets
- Locale decimal separators
- Stray whitespace
- Never depend on "active sheet" behavior

### Writing Excel Files
**Output Quality Requirements:**
- Consistent styling (header styles, column widths, number formats)
- Freeze panes, filters, table formatting where appropriate
- Correct formulas with intentional relative/absolute references
- Formatting logic separated from business logic

**Template Mode:**
- Write data while preserving existing styles
- Do not break named ranges or table definitions

### Large File Handling
- Avoid cell-by-cell operations
- Write arrays/rows in bulk
- For huge datasets: consider CSV + Excel summary workbook

---

## 🧪 Testing Strategy

All features must include tests covering:
- ✅ **Happy path**: Expected inputs produce expected outputs
- ✅ **Invalid schema**: Proper error handling for malformed data
- ✅ **Empty file**: Graceful handling of edge cases
- ✅ **Large dataset**: Performance smoke tests

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_excel_adapter.py

# Run with type checking
mypy .
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip or poetry for dependency management

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd conciliator_softseguros_celer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Or if using poetry:
poetry install
```

### Configuration
1. Copy `.env.example` to `.env`
2. Update environment variables:
   ```
   DATABASE_URL=postgresql://user:pass@localhost/dbname
   LOG_LEVEL=INFO
   OUTPUT_DIR=./output
   ```

---

## 📝 Coding Standards (Non-Negotiable)

### General Rules
- ✅ Python 3.x with **type hints everywhere** (mypy-friendly)
- ✅ Functions: small, pure where possible, single responsibility
- ✅ Use `pathlib.Path`, not raw strings for paths
- ✅ No hard-coded environment values: use config
- ✅ Consistent error handling: domain-specific exceptions
- ✅ Never swallow exceptions silently

### Logging
```python
import logging

logger = logging.getLogger(__name__)

# Include context in logs
logger.info("Processing file", extra={
    "file_name": file_path.name,
    "correlation_id": correlation_id
})
```

### Error Handling
```python
# Good: Specific exceptions
from domain.exceptions import InvalidExcelSchemaError

if not validate_schema(workbook):
    raise InvalidExcelSchemaError(
        f"Missing required sheet: {required_sheet}"
    )

# Bad: Generic or swallowed exceptions
try:
    process_file()
except Exception:
    pass  # ❌ NEVER DO THIS
```

---

## 🔐 Security Guidelines

- ❌ Never use `eval()` on Excel content
- ❌ Never execute macros from untrusted sources
- ✅ Sanitize all file paths
- ✅ Validate upload file extensions and sizes
- ✅ Use parameterized queries for database operations
- ✅ Handle sensitive data (passwords, keys) via environment variables

---

## 📚 Development Workflow

### Before Committing
1. **Format code**: `black . && ruff check --fix .`
2. **Type check**: `mypy .`
3. **Run tests**: `pytest`
4. **Check coverage**: Ensure new code has >80% coverage

### Adding New Dependencies
When adding a new library:
1. Justify it in 1-2 sentences (in PR description)
2. Keep it minimal
3. Update `requirements.txt` or `pyproject.toml`
4. Update lockfile if applicable

### Feature Development Checklist
- [ ] Plan outlined (3-7 bullets)
- [ ] Files to change/create identified
- [ ] Code follows type hints and standards
- [ ] Excel outputs are deterministic
- [ ] Tests written (happy path + edge cases)
- [ ] Logs include meaningful context
- [ ] Error handling covers all paths
- [ ] Documentation updated

---

## 📖 Usage Examples

### Reading Excel
```python
from pathlib import Path
from adapters.excel_reader import ExcelReader
from schemas.insurance_data import InsuranceSchema

reader = ExcelReader()
data = reader.read_file(
    file_path=Path("input/data.xlsx"),
    schema=InsuranceSchema
)
```

### Writing Excel
```python
from adapters.excel_writer import ExcelWriter
from domain.report_generator import ReportGenerator

generator = ReportGenerator()
report_data = generator.generate_monthly_report(data)

writer = ExcelWriter()
writer.write_report(
    data=report_data,
    output_path=Path("output/report_2026_01.xlsx"),
    template="monthly_template"
)
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Excel file is corrupted after generation**
- Check for concurrent writes to the same file
- Ensure proper file closing with context managers
- Verify no special characters in sheet names

**Issue: Performance degradation with large files**
- Profile with `cProfile` to identify bottlenecks
- Consider chunked processing
- Use bulk operations instead of row-by-row

**Issue: Date formatting inconsistencies**
- Always use timezone-aware datetime objects
- Set explicit number formats for date columns
- Test across different locale settings

---

## 📞 Support & Contact

For questions or issues:
- Create an issue in the repository
- Contact: SEGUROS UNIÓN - Automation Team

---

## 📄 License

[Specify your license here]

---

## 🚦 Project Status

**Status**: Active Development
**Last Updated**: January 16, 2026

---

## 🎓 Validation Protocol

Before finalizing any feature, verify:
- ✅ Matches existing project patterns?
- ✅ Types correct and exceptions handled?
- ✅ Excel sheets, names, formats deterministic?
- ✅ Outputs stable across OS/timezones/locales?
- ✅ Tests cover all scenarios?

---

**Ready to build production-grade Excel automation. Let's make it happen! 🚀**
