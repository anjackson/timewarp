from mitmproxy.script import concurrent
from mitmproxy import ctx



@concurrent
def http_connect(flow):
    ctx.log.info("CONNECT FLOW request: %s" % flow.request)
    # Strip the https so upstream requests are http only:
    flow.request.scheme = "http"
    flow.request.port = 80
    print("CONNECT FLOW request: %s" % flow.request)

@concurrent
def request(flow):
    print("FLOW request: %s" % flow.request)
    # Strip the https so upstream requests are http only:
    flow.request.scheme = "http"
    print("FLOW request: %s" % flow.request)
    flow.live.change_upstream_proxy_server('192.168.45.25:8090')


