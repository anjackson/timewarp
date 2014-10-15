import time
from libmproxy.script import concurrent

@concurrent
def request(context, flow):
    #print "handle request: %s - %s" % (flow.request.host, flow.request.path)
    # http://web.archive.org/web/19981212031357
    if not "id_/http" in flow.request.path:
	    flow.request.path = "/web/19981201052808id_/http://%s%s" % (flow.request.host, flow.request.path)
    flow.request.scheme = "http"
    flow.request.host = "web.archive.org"
    flow.request.headers["Host"] = ["web.archive.org"]
