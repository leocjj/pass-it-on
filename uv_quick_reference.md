# UV - Quick Reference

Brief overview of the key steps and commands for using `uv` in your Python projects.

It covers installation, project creation, dependency management, Python version handling, and other useful options.

Whether you're setting up a new project or managing dependencies, this guide will help you get started quickly and efficiently.

## TL;DR


```bash
    # Install 'uv' on macOS, Linux or WSL (recommended)
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Install 'uv' on Windows
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # Install 'uv' on Windows with ThreatLocker
    # This change default installation paths to use a different directory
    $env:UV_PYTHON_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\python"
    powershell -ExecutionPolicy ByPass -c {$env:UV_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin"; irm https://astral.sh/uv/install.ps1 | iex}

    # restart your shell (i.e. close and open it again)

    # To work with a git cloned project, do this inside the cloned folder
    uv sync
    uv run <file.py>

    # To create a new project
    uv init <project_dir>
    cd <project_dir>
    uv run .\hello.py
    uv add <python_package_name_1> <python_package_name_2> ...
    uv run <file.py>
```

## Long Story

1. **Installing uv**

    ```bash
    # On macOS and Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # On Windows with ThreatLocker - Change default installation paths
    $env:UV_PYTHON_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\python"
    powershell -ExecutionPolicy ByPass -c {$env:UV_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin"; irm https://astral.sh/uv/install.ps1 | iex}

    # With pip
    pip install uv

    # Update uv
    uv self update
    ```

1. **Create a new Python project with one of these three options**

    ```bash
    mkdir <project_dir>
    cd <project_dir>
    uv init

    uv init <project_dir>
    cd <project_dir>

    # In case a different python version is needed
    uv init <project_dir> --python 3.12
    cd <project_dir>
    ```

1. **Create and test the Python environment**

    ```bash
    # It's created automatically when a Python file is executed.
    # Doesn't need to be activated or deactivated, uv use a local .venv folder
    uv run .\hello.py
    ```


1. **Working with dependencies**

    ```bash
    # To work with a git cloned project, do this inside the cloned folder
    uv sync

    # To add a new dependency (version number is optional, install the latest)
    uv add <python_package_name>

    # To add a new dependency, upgrade, or downgrade to a specific version
    # Operators: ~= == != <= >= < > ===
    uv add <python_package_name>=='0.115'

    # To export the project's lockfile to a requirements.txt file
    uv export --format requirements-txt > requirements.txt
    
    # To add dependencies from a requirements.txt file to the actual project
    uv add -r requirements.txt

    # To remove a dependency (and its internal dependencies)
    uv remove <python_package_name>

    # To view the dependency tree for the project
    uv tree
    
    # A simple update for a dependency to latest compatible version
    uv remove <python_package_name>
    uv add <python_package_name>
    ```

1. **Installing and managing Python itself**

    ```bash
    # Set a different directory for python binary installations. Default is $env:APPDATA, where APPDATA=C:\Users\<windows_user>\AppData\Roaming
    $env:UV_PYTHON_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\python"

    # When a new project is created, uv install and assign the latest version
    # of CPython available. If a different version is needed, install it with:
    uv python install 3.11 3.12 pypy@3.10

    # View available Python versions to use
    uv python list

    # Execution using a different Python version
    uv run --python 3.12 -- python
    uv run --python 3.13 <file.py>
    uv run --python pypy@3.10 <file.py>
    ```

1. **Other options**

    ```bash
    # uv use pyproject.toml file to specify the main dependencies of the project,
    # and the uv.lock file to specify all dependencies with hashes to create a
    # reproducible environment always.

    # The pyproject.toml file can be modified to remove dependency restrictions
    # and attempt to update the package to the latest compatible version.
    uv lock --upgrade-package <python_package_name>

    # Sync the project's dependencies with the environment.
    # For example, when cloning a project we need to sync the environment.
    uv sync

    # Create a lockfile for the project's dependencies.
    uv lock

    # Build the project into distribution archives.
    uv build
    
    # Publish the project to a package index.
    uv publish
    
    # Connect local repository created after 'uv init', with a remote (GitHub) repository
    git remote add origin git@github.com:<user>/<repo>.git
    git push -u origin main
    
    # To check/set environment variables in Powershell
    dir env:
    $env:UV_PYTHON_INSTALL_DIR
    $env:UV_PYTHON_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\python"

    # To add C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin to your PATH, either restart your shell or run:
    set Path=C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin;%Path%   (cmd)
    $env:Path = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin;$env:Path"   (powershell)
    
    # To know the python and tools binaries directories
    uv python dir
    uv tool dir
    
    # To uninstall
    uv cache clean
    rm -r "$(uv python dir)"
    rm -r "$(uv tool dir)"
    $ rm $HOME\.local\bin\uv.exe
    $ rm $HOME\.local\bin\uvx.exe

    # Others environment variables
    $env:UV_INSTALL_DIR =        "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin";
    $env:UV_PYTHON_BIN_DIR =     "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\bin\python";
    $env:UV_PYTHON_INSTALL_DIR = "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\python";
    $env:UV_CACHE_DIR =          "C:\Users\<windows_user>\OneDrive - ENDAVA\EnDev\.local\uv\cache";
    ```

## References

https://docs.astral.sh/uv/getting-started/installation/

https://docs.astral.sh/uv/reference/cli/

https://pypi.org/project/uv/

https://github.com/astral-sh/uv
