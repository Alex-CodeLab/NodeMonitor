Client for LNM

      Usage:
          Client.py [-hvd]

      Options:
          -d, --debug     Enable debugmessages
          -h, --help      Show this help.
          -v, --version   Show version.


start:
     python Client.py


`client.conf` contains the configuration for this client.
To activate one of the modules in the `modules` folder,
add it to `client.conf` to start sending, and as well to `server.conf`
to accept data on the server side.

A restart is needed when changes in the config were made.
