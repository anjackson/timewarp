from mitmproxy.script import concurrent


@concurrent
def request(flow):
    if flow.request.method == "CONNECT":
        # If the decision is done by domain, one could also modify the server address here.
        # We do it after CONNECT here to have the request data available as well.
        return

    # Strip the https so upstream requests are http only:
    flow.request.scheme = 'http'
    flow.request.port = 80

    print("Requesting %s..." % flow.request.url)

