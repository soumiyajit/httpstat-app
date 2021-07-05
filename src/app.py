import concurrent.futures, os, requests
from prometheus_client import Gauge, make_wsgi_app
from wsgiref.simple_server import make_server

state = Gauge('httpstat_url_up',
                    'httpstat URL state', ['url'])
resp = Gauge('httpstat_url_resp_ms',
                    'httpstat URL resp in ms', ['url'])

class verify_url:
    def __init__(self,urls,timeoutSec,state,resp):
        self.urls = urls
        self.timeoutSec = timeoutSec
        self.state = state
        self.resp = resp

    def __process_request(self,url):
        try:
            r = requests.get(url, timeout=self.timeoutSec)
            respTime = round(r.elapsed.total_seconds()*1000,2)
            return [respTime, r.status_code, url]
        except Exception as err:
            raise Exception(err)

    def request_loop(self):
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(self.__process_request, url) for url in self.urls]

                for f in concurrent.futures.as_completed(results):
                    self.resp.labels(f.result()[2]).set(f.result()[0])
                    if f.result()[1] == 200:
                        self.state.labels(f.result()[2]).set(1)
                    else:
                        self.state.labels(f.result()[2]).set(0)
        except Exception as err:
            raise Exception(err)

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        global verifyUrlObj
        verifyUrlObj.request_loop()
        metrics_app = make_wsgi_app()
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'The httpstat server is reachable !! ']

if __name__ == '__main__':
    urls = os.getenv('URLS').split(',')
    timeoutSec = int(os.getenv('TIMEOUT'))
    verifyUrlObj = verify_url(urls,timeoutSec,state,resp)

    port = int(os.getenv('PORT') or 8000)
    httpd = make_server('0.0.0.0', port, my_app)
    print("Serving on port {}".format(port))
    httpd.serve_forever()
