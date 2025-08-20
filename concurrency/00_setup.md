# Basic setup instructions


## Install Python using uv

```shell
# On WSL, macOS or Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other installation options please go to [uv_quick_reference.md](https://github.com/leocjj/pass-it-on/blob/main/uv_quick_reference.md)

## Clone the repository and execute the scripts

```shell
    # Clone the repository
    git clone https://github.com/leocjj/pass-it-on/
    cd .\pass-it-on\concurrency\

    # Execute the scripts
    uv run 01_intensive_cpu.py
    uv run 02_intensive_io.py
```
