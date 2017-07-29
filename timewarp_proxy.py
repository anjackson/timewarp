import time

from mitmproxy.script import concurrent


@concurrent
def request(flow):
    '''
    Here we intercept the request and use the memento_client library to locate an archived version of the page, resolving all redirects (default behaviour of the memento_client library. Then we replace the requested URL with that one, and do any necessary patching up afterwards in the response handler.
    '''
    print("handle request: %s%s" % (flow.request.host, flow.request.path))
    # http://web.archive.org/web/19981212031357
    if not "id_/http" in flow.request.path:
	    flow.request.path = "/web/19981201052808id_/http://%s%s" % (flow.request.host, flow.request.path)
    flow.request.scheme = "https"
    flow.request.host = "web.archive.org"
    flow.request.port = 443
    flow.request.headers["Host"] = "web.archive.org"

@concurrent
def response(flow):
    print("handle response: %s %s" % (flow.response, flow.response.headers))

