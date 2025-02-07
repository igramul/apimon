# APIM Service Monitor (APIMON)

This is a Raspberry PI Zero based service Monitor written in Python.

A Flask web server for monitoring the APIM Jira service board and display the
number of open tickets on a neopixel led stripe.

## Initial Project Setup

1. install the needed python modules `make install`
2. create an initial git commit (if you start from scratch)
3. create the first version tag like `git tag 0.1.0`
4. start server be invoke `make`


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


## Setup automatic update

Configure a cronjob to execute the script `./bin/update_and_restart.sh`

For example like this:

    */5 * * * * /path/to/update_and_restart.sh >> /path/to/update_and_restart.log 2>&1


## Configure Unattended OS Upgrades

See this link: https://wiki.debian.org/UnattendedUpgrades
