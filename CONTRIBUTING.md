# Contributing to JSON Normalize

Thank you for your interest in contributing to JSON Normalize! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.7+
- Git
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/json-normalize.git
cd json-normalize

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements.txt  # Includes dev dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=json_normalize --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run tests with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black json_normalize/

# Check linting
flake8 json_normalize/

# Type checking
mypy json_normalize/
```

## Development Workflow

### 1. Choose an Issue

- Check the [Issues](https://github.com/NguyenVanTien204/Json_Normalize/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
# Create and switch to a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-number-description
```

### 3. Make Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Commit Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add new normalization feature

- Add support for custom separators
- Handle edge cases in array processing
- Add comprehensive tests

Closes #123"
```

### 5. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints for function parameters and return values

### Naming Conventions

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods/attributes: `_leading_underscore`

### Documentation

- Use docstrings for all public functions, classes, and modules
- Follow [Google style](https://google.github.io/styleguide/pyguide.html#381-docstrings) for docstrings
- Include type hints in function signatures
- Document parameters, return values, and exceptions

**Example:**
```python
def normalize_json(obj: dict, sep: str = ".") -> List[Dict]:
    """Normalize a JSON object by flattening nested structures.

    Args:
        obj: The JSON object to normalize
        sep: Separator for flattened keys

    Returns:
        List of normalized dictionaries

    Raises:
        JsonNormalizeError: If normalization fails

    Examples:
        >>> data = {"user": {"name": "John"}}
        >>> normalize_json(data)
        [{"user.name": "John"}]
    """
```

## Testing Guidelines

### Test Structure

- Tests are located in the `tests/` directory
- Test files should be named `test_*.py`
- Test classes should be named `Test*`
- Test methods should be named `test_*`

### Writing Tests

```python
import pytest
from json_normalize.core import flatten_dict

class TestFlattenDict:
    def test_basic_flattening(self):
        """Test basic dictionary flattening."""
        data = {"user": {"name": "John", "age": 30}}
        result = flatten_dict(data)
        expected = [{"user.name": "John", "user.age": 30}]
        assert result == expected

    def test_empty_dict(self):
        """Test handling of empty dictionaries."""
        result = flatten_dict({})
        assert result == [{}]

    @pytest.mark.parametrize("input_data,expected", [
        ({"a": 1}, [{"a": 1}]),
        ({"a": {"b": 2}}, [{"a.b": 2}]),
    ])
    def test_parametrized_flattening(self, input_data, expected):
        """Test flattening with multiple inputs."""
        result = flatten_dict(input_data)
        assert result == expected
```

### Test Coverage

- Aim for >90% code coverage
- Test edge cases and error conditions
- Use fixtures for common test data
- Mock external dependencies

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=json_normalize --cov-report=term-missing

# Run specific tests
pytest tests/test_core.py::TestFlattenDict::test_basic_flattening

# Run tests in verbose mode
pytest -v

# Run tests and stop on first failure
pytest -x
```

## Documentation

### Updating Documentation

- Update docstrings when changing function signatures
- Add examples for new features
- Update the README for major changes
- Keep API documentation in sync

### Building Documentation

```bash
# Generate API documentation (if using Sphinx)
make docs

# Or manually update docs/
# Update relevant .md files in docs/ directory
```

## Pull Request Process

### Before Submitting

1. **Tests Pass**: Ensure all tests pass locally
2. **Code Quality**: Run linting and formatting
3. **Documentation**: Update relevant documentation
4. **Changelog**: Add entry to CHANGELOG.md

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] Changelog updated

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: At least one maintainer reviews the code
3. **Approval**: PR is approved and merged
4. **Deployment**: Changes are deployed to production

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, etc.
- **Code Sample**: Minimal code to reproduce the issue

### Feature Requests

For feature requests, please include:

- **Description**: Clear description of the proposed feature
- **Use Case**: Why this feature would be useful
- **Implementation Ideas**: Any thoughts on implementation
- **Alternatives**: Alternative approaches considered

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Maintain professional communication

### Getting Help

- Check existing issues and documentation first
- Use clear, descriptive titles for issues
- Provide context and examples
- Be patient when waiting for responses

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- GitHub's contributor insights
- Release notes for significant contributions

Thank you for contributing to JSON Normalize! 🎉
