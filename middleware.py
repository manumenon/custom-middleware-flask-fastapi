from werkzeug.wrappers import Request, Response, ResponseStream
import requests

TOKEN_AUTH_SERVICE_URL = "http://127.0.0.1:5001"


class middleware():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if  request.path not in ["/", "/healthcheck"]:
            token = request.headers.get('Authorization', "").split(" ")[-1]

            if not token:
                res = Response(u'Authorization failed', mimetype='text/plain', status=401)
                return res(environ, start_response)
            jwt_res = requests.post(TOKEN_AUTH_SERVICE_URL, json={"token": token})
            if jwt_res.status_code != 200:
                res = Response(u'Authorization failed', mimetype='text/plain', status=401)
                return res(environ, start_response)
        return self.app(environ, start_response)
