# API Management Raspberry PI based Service Monitor (APIMON) Service in Flask

A Flask web server for monitoring the APIM Jira service board and display the
number of open tickets on a neopixel led stripe.

## Initial Project Setup

1. install the needed python modules `make install`
2. create an initial git commit
3. create the first version tag like `git tag 0.1.0`
4. run make


## Setup automatic start

    sudo cp apimon.service /etc/systemd/system/

    sudo systemctl daemon-reload
    sudo systemctl enable apimon
    sudo systemctl start apimon
    sudo systemctl status apimon

LRead the logs: `journalctl -u apimon`