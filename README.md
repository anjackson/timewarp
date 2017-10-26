Memento Proxy
=============

This system sets up a Memento-compliant web proxy for proxy-mode playback of web resources. It does this by consulting one or more Memento TimeGates, and uses them to find copies of resouces from web archives across the world. Proxy-mode allows for very high fidelity playback.

For example, if the browser requests:

    http://news.bbc.co.uk/

...with an `Accept-Datetime` header in 1998, the Memento TimeGate will look for the closest match. The might result redirecting the request to a Wayback instance:

    http://web.archive.org/web/19981201052808id_/http://news.bbc.co.uk/

...using an embedded timestamp to determine which time period you are browsing, with the ```id_``` suffix which instructs Wayback _not_ to modify the document before returning it (i.e. no link re-writing).


Quick start
-----------

Step 1: Install [MITM Proxy](http://mitmproxy.org) on a suitable server (we'll call it ```servername``` here):

    $ pip install -r requirements.txt

Step 2: Run the proxy with the timewarp [inline script](http://mitmproxy.org/doc/scripting/inlinescripts.html):

    $ mitmdump -s timewarp_proxy.py
    $ mitmdump -p 8090 -s timewarp_proxy.py --no-upstream-cert

Step 3: Set your web browser to use ```servername:8080``` as your web proxy.


OTHER MODE

    $ mitmdump -U http://openwayback.proxy.mode.service:8090/ -s timewarp_proxy_owb.py

Issues
------

- Add reference to https://github.com/mementoweb/py-memento-client in the text above.
- Hm, should check if this has already been done.
- The redirects to different timestamps cause a fair degree of confusion, although it all pretty much works. Perhaps it is possible to handle the redirects in the proxy rather than passing them back to the client? See e.g. [redirect_requests.py](https://github.com/mitmproxy/mitmproxy/blob/master/examples/redirect_requests.py)
- Remove hard-coded 1998 timestamp!
- Look up across multiple archives? Leveraging Memento?
