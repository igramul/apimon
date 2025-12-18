# APIM Service Tickets Monitor (APIMON)

This is a Raspberry PI Zero based Jira Service Tickets Monitor written in Python.

A Flask web server for monitoring the APIM Jira Service Tickets board and display the
number of open tickets on a neopixel led stripe.

## LED Display Options

The project supports three different LED display modes:

1. **Hardware LEDs (Raspberry Pi)**: Uses real NeoPixel LED strips via `rpi_ws281x` or `adafruit-circuitpython-neopixel`
2. **Qt GUI (Development)**: Graphical display using PySide6 - automatically used on Mac/PC when PySide6 is installed
   - **LEDs are arranged vertically** with LED 0 at the bottom
   - Windows are positioned side-by-side for multiple strips
3. **Console (Fallback)**: Text-based console output - used when Qt is not available

The appropriate display mode is automatically selected based on the platform and available libraries.

### Testing the Qt Display

There are multiple test scripts to verify the Qt display functionality:

1. **Vertical Layout Test** - Verifies LED 0 is at bottom:
   ```bash
   python demo/test_vertical_layout.py
   ```

2. **Simple Test** - Basic QtPixel functionality:
   ```bash
   python demo/test_qtpixel_simple.py
   ```

3. **NeoPixelController Test** - Tests integration with controller:
   ```bash
   python demo/test_neopixel_controller.py
   ```

4. **APIMON Simulation** - Full simulation without Flask/Jira:
   ```bash
   python demo/simulate_apimon.py
   ```

5. **Animated Demo** - Shows animated LED strips:
   ```bash
   python demo/demo_qtpixel.py
   ```

For detailed debugging information, see `QTPIXEL_DEBUGGING.md`, `QTPIXEL_VERTICAL.md`, and `QTPIXEL_FIX.md`
in folder doc/QtPixel.

## Initial Project Setup (only needed if you start from scratch)

1. install the needed python modules `make install`
2. create an initial git commit (if you start from scratch)
3. create the first version tag like `git tag 0.1.0`
4. start server be invoke `make start`

## Install and clone Project from GitHub

    git clone <https-projekt-url>

Setup .env file with OAuth client-id and secret.
Copy .env-example to .env and fill in valid data.

## Setup automatic start

Copy the service config file into place:

    sudo cp etc/apimon.service /etc/systemd/system/

Edit the file to change the path to the apimon directory.

Setup and start the service:

    sudo systemctl daemon-reload
    sudo systemctl enable apimon
    sudo systemctl start apimon
    sudo systemctl stop apimon
    sudo systemctl status apimon
    sudo systemctl restart apimon

Read the logs:

    journalctl -fu apimon


## Setup automatic update (untested and not yet recommended)

Configure a cronjob to execute the script `./bin/update_and_restart.sh`

For example like this:

    */5 * * * * /path/to/update_and_restart.sh >> /path/to/update_and_restart.log 2>&1


## Configure Unattended OS Upgrades

See this link: https://wiki.debian.org/UnattendedUpgrades
