
[WIP]
Work in progress.

(basic functionality/framework works, but needs modules and a frontend)

------------------------

Lightweight Server/Node monitor
---------------

A realtime, super lightweight Framework for monitoring servers, nodes.

Can be used with or without a frontend dashboard (using Flask)


Goals:
- simple and efficient
- small footprint (few external libraries)
- easy to audit (less then 500lines of code)
- super easy to extend
- Push messages from Clients instead of Pull by server
- multiprocessing, async (Trio)
- extremely low cpu/memory usage
- capable of running on SBC or IoT devices
- (modules for BTC/Lightning)
- (alerting mechanism)

------------

     ____________                _____________  <--Module1. (interval)
     |           | <--- push ----| Node 1    |  <--Module2. (interval)
     | Collector |               _____________                 
     |           | <----push ----| Node 2    |  <--Module2. (interval)
     -------------               _____________  <--Module1. (interval)     
       |      |                                   
       |      |
       |      ----> [ batch write rrd DB ]
       websocket--> [ browser ]


------------
add a module:

     create a new function in client/modules/
     add it to modules in client.conf
     add it to modules in server.conf

-----------
install:

     pip install nnpy flask

See the `client` and `server` folders.

------------

Contributing
This is a open-source, community project.
Build whatever you want. Start with creating a ticket that describes a problem.


---------

todo:
 - (lightweight) frontend
 - fix tests
 - add modules
 - rrd for hour/day
 - write tests for websockets
