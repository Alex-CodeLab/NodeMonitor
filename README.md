
[WIP]
Work in progress.

(basic functionality/framework works, but needs modules and better frontend)

------------------------

Lightweight Server/Node monitor
---------------

A realtime, super lightweight Framework for monitoring servers, nodes.

Can be used with or without a frontend dashboard (using Flask)


Goals:
- simple and efficient
- small footprint (few external libraries)
- easy to audit
- super easy to extend
- Push messages from Clients instead of Pull by server
- multiprocessing, async (Trio)
- very low cpu/memory usage
- capable of running on SBC devices (or IoT with some changes)
- automatically add new graphs (without extra coding)
- (modules for BTC/Lightning)
- (alerting mechanism)

------------

     ____________                _____________  <--Module1. (interval)
     |           | <--- push ----| Node 1    |  <--Module2. (interval)
     | Collector |               _____________                 
     |           | <----push ----| Node 2    |  <--Module2. (interval)
     -------------               _____________  <--Module1. (interval)     
       |      |                   ...                
       |      |
       |      ----> [ batch write rrd DB ]
       websocket--> [ browser ]


------------
#### modules
add a module:

     create a new function in client/modules/
     add it to modules in client.conf
     add it to modules in server.conf

-----------
Install:

(create a virtualenv , clone the repo.)

     pip install -r requirements.txt

Run:

  See README in the `client` and `server` folders.

------------

##### Contributing

This is a open-source, community project.
Build whatever you want. Start with creating a ticket that describes a problem.


---------

todo:
 - (lightweight) frontend
 - fix tests
 - add modules
 - rrd for hour/day
 - write tests for websockets
