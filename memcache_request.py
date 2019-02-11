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