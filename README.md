
[WIP]
Work in progress.

(basic functionality/framework works, but needs  modules and a frontend)

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
- extremely low cpu/memory usage
- capable of running on SBC or IoT devices
- (modules for BTC/Lightning)
- (alerting mechanism )


------------
add a module:

     create a new function in client/modules/
     add it to modules in client.conf
     add it to modules in server.conf

-----------
install:

     pip install nnpy flask pyzmq

See the `client` and `server` folders.

------------

Contributing
This is a open-source, community project.
Build whatever you want. Start with creating a ticket that describes the problem.


---------

todo:
    - (lightweight) frontend
    - fix tests
    - add modules
    - write tests for websockets
