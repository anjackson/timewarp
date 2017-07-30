import time
import datetime
from memento_client import MementoClient

from mitmproxy.script import concurrent


@concurrent
def request(flow):
    '''
    Here we intercept the request and use the memento_client library to locate an archived version of the page, resolving all redirects (default behaviour of the memento_client library. Then we replace the requested URL with that one, and do any necessary patching up afterwards in the response handler.
    '''
    print("handle request: %s%s" % (flow.request.host, flow.request.path))
    # http://web.archive.org/web/19981212031357
    if not "id_/http" in flow.request.path:
        dt = datetime.datetime(2010, 4, 24, 19, 0)
        uri = flow.request.url
        mc = MementoClient()
        memento_uri = mc.get_memento_info(uri, dt).get("mementos").get("closest").get("uri")[0]
        flow.request.url = memento_uri

@concurrent
def response(flow):
    print("handle response: %s %s" % (flow.response, flow.response.headers))

