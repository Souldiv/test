import os
import tornado.auth
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
import tornado.escape

define("port", default=8000, help="runs on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write({"status_code": status_code, "status_message": self._reason})
        elif status_code == 500:
            self.write({"status_code": status_code, "status_message": "Scraping Error"})
        elif status_code == 400:
            self.write({"status_code": status_code, "status_message": self._reason})


class ErrorHandler(tornado.web.ErrorHandler, IndexHandler):
    pass


class test(tornado.web.RequestHandler):
    async def get(self):
        result = self.request.get_arguments()
        if(result is None):
            self.write(json.dumps({
                'status_code': 140,
                'status_message': 'in the none',
                'kappa': None
                }))
        print(result)
        self.write(json.dumps({ 'status_code': 200,
            'status_message': "works",
            'kappa': result
            }
            ))

    
    async def post(self):
        result = tornado.escape.json_decode(self.request.body)
        print(result)
        if(result is None):
            self.write(json.dumps({
                'status_code': 140,
                'status_message': 'in the none',
                'kappa': None
                }))
        self.write(json.dumps({
            'status_code': 200,
            'kappa': result,
            'status_message': 'works'
            }))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        'default_handler_class': ErrorHandler,
        'default_handler_args': dict(status_code=404)
    }
    app = tornado.web.Application(
        handlers=[
            (r"/", test)
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(os.environ.get("PORT",options.port))
    print("listening on port",8000)
    tornado.ioloop.IOLoop.instance().start()
