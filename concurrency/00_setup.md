# Basic setup instructions


## Install Python using uv

    https://docs.astral.sh/uv/getting-started/installation/
    https://docs.astral.sh/uv/reference/cli/
    https://github.com/astral-sh/uv

```shell
# On macOS, Linux, and WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# On Windows with ThreatLocker - Change default installation paths

$env:UV_PYTHON_INSTALL_DIR = "C:\<one_drive_dir>\EnDev\.local\uv\python"

powershell -ExecutionPolicy ByPass -c {$env:UV_INSTALL_DIR = "C:\<one_drive_dir>\EnDev\.local\uv\bin"; irm https://astral.sh/uv/install.ps1 | iex}
```

## Clone the repository and execute the scripts

```shell
    # Clone the repository
    git clone https://github.com/en-lcalderon/pass-it-on.git
    cd .\pass-it-on\concurrency\

    # Create a virtual environment
    uv sync

        or

    uv init --python 3.12
    uv add aiohttp
    
    # Execute the scripts
    uv run 01_intensive_cpu.py
    uv run 02_intensive_io.py
```
