import socketserver
import sys
from memcache_request import MemcacheRequest
from database import Database

db = Database()  # global object for sharing db when present


class MemcachedRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our Memached server.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        memcache_request = MemcacheRequest(self.request)
        memcache_request.execute()


if __name__ == "__main__":
    HOST, PORT = "localhost", 11211

    # Initialize database
    if sys.argv[2]:
        db.initialize(sys.argv[2])

    # Create the server, binding to localhost on port 11211
    with socketserver.TCPServer(
            (HOST, PORT), MemcachedRequestHandler) as server:
        # Activate the server
        server.serve_forever()
