import re
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
        # TO DO Parse any supplied 'Accept-Datetime' header and use that...
        dt = datetime.datetime(1996, 1, 1, 1, 0)
        adt = flow.request.headers.get('Accept-Datetime', None)
        if adt:
          dt = datetime.datetime.strptime(adt, '%a, %d %b %Y %H:%M:%S GMT')
        uri = flow.request.url
        timegate = "https://www.webarchive.org.uk/wayback/archive/"
        mc = MementoClient(timegate_uri=timegate, check_native_timegate=False)
        #mc = MementoClient()
        print("Getting mementos...")
        try:
          mementos = mc.get_memento_info(uri, dt).get("mementos")
          if mementos:
            if 'closest' in mementos:
               flow.request.url = mementos.get("closest").get("uri")[0]
            elif 'memento' in mementos:
               flow.request.url = mementos.get("closest").get("uri")[0]
            # Need to patch the id_ into the url:
            flow.request.url = re.sub(r"\/(\d{14})\/",r"/\1id_/", flow.request.url )
        except Exception as e:
          print(e)
          pass

        print("Getting %s..." % flow.request.url)
            

@concurrent
def response(flow):
    print("handle response: %s %s" % (flow.response, flow.response.headers))

