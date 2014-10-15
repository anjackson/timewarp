timewarp
========

Making it easier to browse the past.

Quick start
-----------

Step 1: Install [MITM Proxy](http://mitmproxy.org) on a suitable server (we'll call it ```servername``` here):

    $ pip install mitmproxy

Step 2: Run the proxy with the timewarp [inline script](http://mitmproxy.org/doc/scripting/inlinescripts.html):

    $ mitmdump -s timewarp_proxy.py

Step 3: Set your web browser to use ```servername:8080``` as your web proxy.

How it works
------------

This web proxy takes incoming HTTP requests and maps them to the [Internet Archive Wayback Machine](http://archive.org/web/). For example, if the browser requests:

    http://news.bbc.co.uk/

The proxy fetches:

    http://web.archive.org/web/19981201052808id_/http://news.bbc.co.uk/

Using an embedded timestamp to determine which time period you are browsing, with the ```id_``` suffix which instructs Wayback _not_ to modify the document before returning it (i.e. no link re-writing).

Issues
------

- The redirects to different timestamps cause a fair degree of confusion, although it all pretty much works. Perhaps it is possible to handle the redirects in the proxy rather than passing them back to the client? See e.g. [redirect_requests.py](https://github.com/mitmproxy/mitmproxy/blob/master/examples/redirect_requests.py)
- Remove hard-coded 1998 timestamp!
- Look up across multiple archives? Leveraging Memento?
