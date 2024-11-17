import os
import subprocess
import sys

def create_env(project_path, env_name="BuildEnv"):
    """
    Creates a Python virtual environment in the specified folder.
    
    Parameters:
        project_path (str): Path to the project folder.
        env_name (str): Name of the environment folder to create (default: 'BuildEnv').
    """
    env_path = os.path.join(project_path, env_name)
    
    # Check if the environment already exists
    if not os.path.exists(env_path):
        print(f"Creating build environment at {env_path}...")
        # Create the virtual environment
        subprocess.run(["python3", "-m", "venv", env_path], check=True)
        print(f"Build environment created at {env_path}.")
    else:
        print(f"Build environment already exists at {env_path}.")
    
    # Upgrade pip inside the virtual environment
    pip_executable = os.path.join(env_path, "bin", "pip")
    subprocess.run([pip_executable, "install", "--upgrade", "pip"], check=True)
    print("Pip upgraded successfully.")

    # Install default dependencies (optional)
    subprocess.run([pip_executable, "install", "wheel"], check=True)
    print("Default dependencies installed.")

if __name__ == "__main__":
    # Ensure the project path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python create_env.py <project_path>")
        sys.exit(1)
    
    # Get the project path from the command-line arguments
    project_path = sys.argv[1]
    create_env(project_path)

