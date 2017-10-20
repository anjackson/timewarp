import re
import time
import requests
import requests.adapters
import datetime
from memento_client import MementoClient
from mitmproxy.script import concurrent

#archive_prefix = "http://timetravel.mementoweb.org/"
#timegate = "http://timetravel.mementoweb.org/timegate/"

#archive_prefix = "https://www.webarchive.org.uk"
#timegate = "https://www.webarchive.org.uk/wayback/archive/"

archive_prefix = "https://web.archive.org"
timegate = "https://web.archive.org/web/"


SLEEP_SECONDS = 10
requests.adapters.DEFAULT_RETRIES = 3

# This is really rather slow...
def get_via_mementos(uri, dt):
    mc = MementoClient(timegate_uri=timegate, check_native_timegate=False)
    # mc = MementoClient()
    print("Getting mementos for %s ..." % uri)
    try:
        mementos = mc.get_memento_info(uri, dt).get("mementos")
        if mementos:
            print("Got mementos for %s ..." % uri)
            if 'closest' in mementos:
                uri = mementos.get("closest").get("uri")[0]
            elif 'memento' in mementos:
                uri = mementos.get("closest").get("uri")[0]
            # Need to patch the id_ into the url:
            uri = re.sub(r"\/(\d{14})\/", r"/\1id_/", uri)
    except Exception as e:
        print(e)
        pass

    return uri

# This is faster...
def get_via_timegate(uri,dt):
    # Find the location header to get the new URI from the timegate:
    #print("Getting memento for %s ..." % uri)
    uri = "%s%s" % (timegate, uri)
    #print("Getting memento using %s ..." % uri)

    # Find the nearest match:
    headers = {'Accept-Datetime': dt, 'User-Agent': 'Timewarp Web Archive Pseudo-proxy (a UK Web Archive experiment)'}
    r = requests.head(uri, headers=headers, allow_redirects=True )
    # Get the final URL
    uri = r.url

    # Need to patch the id_ into the url:
    uri = re.sub(r"\/(\d{14})\/", r"/\1id_/", uri)

    return uri


@concurrent
def request(flow):
    '''
    Here we intercept the request and use the memento_client library to locate an archived version of the page, resolving all redirects (default behaviour of the memento_client library. Then we replace the requested URL with that one, and do any necessary patching up afterwards in the response handler.
    '''
    print("handle request: %s%s" % (flow.request.host, flow.request.path))
    uri = flow.request.url
    # http://web.archive.org/web/19981212031357
    if not uri.startswith(archive_prefix):
        # TO DO Parse any supplied 'Accept-Datetime' header and use that...
        dt = datetime.datetime(1996, 1, 1, 1, 0)
        adt = flow.request.headers.get('Accept-Datetime', None)
        if adt:
          dt = datetime.datetime.strptime(adt, '%a, %d %b %Y %H:%M:%S GMT')
          flow.request.url = get_via_timegate(uri, adt)
          print("Re-routing to %s for %s..." % (flow.request.url, uri))

    print("Requesting %s..." % flow.request.url)
            

@concurrent
def response(flow):
    if flow.response.status_code == 429:
        print("Sleeping...")
        time.sleep(SLEEP_SECONDS)
    flow.response.headers.pop("Content-Security-Policy", None)
    if flow.response.headers.get('Location', None):
       print("NO LOCATION HEADERS SHOULD BE RETURNED FOR ARCHIVED URLS! - url %s -> %s" % (flow.request.url,flow.response.headers['Location']) )
    #print("handle response: %s %s" % (flow.response, flow.response.headers))

