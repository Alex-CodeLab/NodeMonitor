

Server.py


        Usage:
          Server.py [-hvdw]

        Options:
          -d, --debug         Enable debugmessages
          -w, --no-webserver  Do not start webserver
          -h, --help          Show this help.
          -v, --version       Show version.


start:
      python Server.py


See `server.config` for options.
To accept messages from Clients, the modulename must exist in the section `modules`