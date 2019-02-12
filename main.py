import socketserver
import sys
from memcached_request import MemcachedRequest
from database import Database

db = Database()  # global object for sharing db when present


class Cache:
    """
    Used to temporarily cache a request.
    """
    waiting = False
    cached_request = None


class MemcachedRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our Memached server.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        if Cache.cached_request:
            memcached_request = Cache.cached_request
            memcached_request.update(self.request)
        else:
            memcached_request = MemcachedRequest(self.request, db)

        response = memcached_request.execute(followup=Cache.waiting)
        self.request.sendall(response.encode())

        # caching request if needed
        if memcached_request.requires_additional_data:
            Cache.cached_request = memcached_request
            Cache.waiting = True
        else:
            Cache.cached_request = None
            Cache.waiting = False


def start_server(host, port):
    print('Initializing server...')
    # initialize db
    db.initialize(sys.argv[2])

    # Create the server, binding to localhost on port
    with socketserver.TCPServer(
            (HOST, PORT), MemcachedRequestHandler) as server:
        print('Accepting requests on %s:%s' % (host, port))
        # Activate the server
        server.serve_forever()
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 11211
    if sys.argv[1] == 'serve' and sys.argv[2]:
        start_server(HOST, PORT)
    else:
        print('usage: python main.py serve database.sqlite')
