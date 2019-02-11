import socketserver


class MemcacheRequest:
    """
    A request object class for our Memached server.
    """

    def __init__(self, request):
        self.request = request.recv(1024).strip().decode('utf-8')

    @property
    def command(self):
        return str(self.request.split(' ')[0])

    def execute(self):
        options = {
            'set': self.set_cache,
            'get': self.get_cache,
            'delete': self.delete_cache,
        }
        options[self.command]()

    def set_cache(self):
        # todo: implement
        print('setting cache')

    def get_cache(self):
        # todo: implement
        print('getting cache')

    def delete_cache(self):
        # todo: implement
        print('deleting cache')


class MemcachedRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our Memached server.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        memcache_request = MemcacheRequest(self.request)
        memcache_request.execute()


if __name__ == "__main__":
    HOST, PORT = "localhost", 12111

    # Create the server, binding to localhost on port 12111
    with socketserver.TCPServer((HOST, PORT), MemcachedRequestHandler) as server:
        # Activate the server
        server.serve_forever()
