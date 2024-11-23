---

# PyEnvBuilder

**PyEnvBuilder** is a simple and efficient tool designed to automate the creation of isolated Python virtual environments for Xcode projects or other development workflows. This project ensures each project has its own dedicated build environment, keeping dependencies clean and conflict-free.

## Features
- **Automatic Virtual Environment Creation**: Creates a `BuildEnv` folder within your project directory using Python’s `venv`.
- **Dependency Management**:
  - Automatically upgrades `pip`.
  - Installs essential tools like `wheel`.
- **Seamless Integration**: Works as part of Xcode’s **External Build System**, or can be run as a standalone script.
- **Lightweight and Flexible**: Keeps your development environment isolated without adding unnecessary overhead.

## Use Cases
- **Isolated Python Build Environments**: Ideal for projects that require Python scripts or tools during the build process.
- **Dependency Management**: Manage project-specific Python dependencies without polluting your global environment.
- **Xcode Integration**: Integrate with Xcode's External Build System for automated setup during builds.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pyenvbuilder.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pyenvbuilder
   ```
3. Ensure `python3` is installed on your system:
   ```bash
   python3 --version
   ```

## Usage
1. **Manual Execution**:
   Run the script to set up a virtual environment in your project folder:
   ```bash
   python3 PythonEnv/create_env.py /path/to/project
   ```

2. **Xcode Integration**:
   - Add the script to your Xcode **External Build System**.
   - Configure the build tool to invoke the script automatically for each build.

## Directory Structure
```plaintext
pyenvbuilder/
├── PythonEnv/
│   └── create_env.py   # Main script for environment setup
├── README.md           # Project documentation
├── LICENSE             # License information
```

## Future Plans
- Add environment cleanup and reset functionality.
- Enhance logging and error handling.
- Build a CLI or GUI for easier interaction.
- Extend support for more advanced Python workflows in Xcode.

## Contributing
Contributions are welcome! Please submit issues or pull requests to help improve this tool.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
