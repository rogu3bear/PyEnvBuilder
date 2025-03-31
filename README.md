---

# PyEnvBuilder

A lightweight Python tool for creating and managing virtual environments in Xcode projects. This tool is designed to be easily integrated into Xcode's build process.

## Features

- Automated virtual environment creation for Xcode projects
- Pre-installation system checks
- Cross-platform support (macOS, Linux)
- Simple CLI interface
- Xcode build script integration
- Comprehensive test coverage (95%)
- Robust error handling and validation

## Pre-Installation Checks

Before creating a virtual environment, PyEnvBuilder performs several safety checks:

- Python Version: Verifies that your Python installation meets the minimum version requirements (3.7+)
- Virtual Environment Support: Ensures the `venv` module is available and working
- Pip Availability: Confirms that pip is installed and functioning correctly
- Xcode Command Line Tools: Verifies installation on macOS systems
- Project Directory: Validates the target directory structure

## Installation

```bash
pip install pyenvbuilder
```

## Usage

### Basic Python Usage

```python
from pyenvbuilder import setup_xcode_project, create_env, cleanup_env

# Set up a complete Xcode project environment
setup_xcode_project("/path/to/xcode/project")

# Create a virtual environment in a specific directory
create_env("/path/to/project")

# Clean up an environment
cleanup_env("/path/to/env", force=True)
```

### Command Line Usage

```bash
# Create a virtual environment in the current directory
python -m pyenvbuilder create .

# Create with custom environment name
python -m pyenvbuilder create . --name custom_env

# Clean up an environment
python -m pyenvbuilder cleanup /path/to/env --force

# Set up Xcode integration
python -m pyenvbuilder xcode /path/to/project
```

### Xcode Integration

1. Add a "Run Script" build phase to your Xcode project
2. Add the following script:

```bash
#!/bin/bash

# Set up Python environment
python -m pyenvbuilder xcode "${PROJECT_DIR}"

# Activate the environment
source "${PROJECT_DIR}/BuildEnv/bin/activate"

# Run your Python scripts here
python "${PROJECT_DIR}/your_script.py"
```

## Requirements

- Python 3.7 or higher
- macOS or Linux
- Xcode (for Xcode integration)
- pip (for package installation)

## Project Structure

```plaintext
pyenvbuilder/
├── py-src/
│   └── pyenvbuilder/
│       ├── __init__.py           # Package initialization and Xcode integration
│       ├── create_env.py         # Environment creation functionality
│       ├── cleanup.py            # Environment cleanup utilities
│       ├── pre_install_check.py  # System requirement verification
│       ├── cli.py               # Command-line interface
│       └── tests/               # Test suite
├── requirements/
│   ├── base.txt                # Core dependencies
│   └── dev.txt                 # Development dependencies
├── README.md                   # Project documentation
└── pyproject.toml             # Project configuration
```

## Development

### Test Coverage

The project maintains high test coverage across all modules:

- `__init__.py`: 94% coverage
- `cleanup.py`: 89% coverage
- `cli.py`: 98% coverage
- `create_env.py`: 85% coverage
- `pre_install_check.py`: 96% coverage

Total coverage: 95% across 619 statements with 42 test cases.

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/pyenvbuilder.git
cd pyenvbuilder

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements/dev.txt

# Install the package in editable mode
pip install -e .

# Run tests
python -m pytest py-src/pyenvbuilder/tests/ -v --cov=pyenvbuilder
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. When contributing:

1. Fork the repository
2. Create a feature branch
3. Add tests for any new functionality
4. Ensure all tests pass and maintain code coverage
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the documentation
2. Look through existing GitHub issues
3. File a new issue with:
   - Your OS and Python version
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Any relevant error messages

## Future Plans

- Add environment cleanup and reset functionality
- Enhance logging and error handling
- Build a GUI for easier interaction
- Extend support for more advanced Python workflows in Xcode
- Add support for custom Python versions
- Implement environment isolation options
- Add dependency management features
