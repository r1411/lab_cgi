from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import db

class MyHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == '/':
            self.path = '/index.html'
        
        if parsed_url.path.endswith(".py"):
            self.path = '/cgi-bin/' + parsed_url.path + '?' + parsed_url.query

        return CGIHTTPRequestHandler.do_GET(self)


def main():
    # db.setup_tables()
    # db.add_test_data()
    server_addr = ('localhost', 8080)
    handler = MyHandler
    handler.cgi_directories = ["/cgi-bin"]
    server = HTTPServer(server_addr, handler)
    server.serve_forever()


if __name__ == '__main__':
    main()