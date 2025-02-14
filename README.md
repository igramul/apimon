# API Management Raspberry PI based Service Monitor (APIMON) Service in Flask

A Flask web server for monitoring the APIM Jira service board and display the
number of open tickets on a neopixel led stripe.


## Initial Project Setup

1. create an initial git commit
2. create the first version tag like `git tag 0.1.0`
3. run make


## Setup automatic start

    sudo cp apim.service /etc/systemd/system/

    sudo systemctl daemon-reload
    sudo systemctl enable apimon.service
    sudo systemctl start apimon.service

