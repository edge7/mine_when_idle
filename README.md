# XMRIG Process Controller

## Overview

This Python script is designed to control the lifecycle of an XMRIG mining process based on user activity. The script checks system idle time and starts or stops the XMRIG process accordingly:

- If the system has been idle for more than 5 minutes, it starts the XMRIG process.
- If the system becomes active again, it stops the XMRIG process.

## Requirements

To run this script, you will need:

- Python 3.x
- The `psutil` Python package for process and system utilities
- The `xprintidle` utility for Xorg, to fetch system idle time

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory and run the following command to install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Note on `xprintidle`

This script relies on the `xprintidle` utility to get the system idle time. This utility is designed to work with Xorg. If you're not using Xorg, you will need to find an alternative way to get system idle time.

## Usage

After installing the requirements, you can run the script using Python:

```bash
python main.py
```

## Running with Systemd

If you'd like to run this script as a systemd service, you can create a new service file, e.g., `xmrig-controller.service`, with the following content:

```ini
[Unit]
Description=Simple Miner
Wants=graphical.target
After=graphical.target

[Service]
Type=simple
User=YOUR_USERNAME
Group=YOUR_GROUP
Environment=DISPLAY=:1
Environment=XMRIG_PATH=/path/to/your/xmrig/folder
WorkingDirectory=/path/to/your/project/folder
ExecStart=/usr/bin/python3 /path/to/your/project/folder/main.py
Restart=always

[Install]
WantedBy=default.target
```

