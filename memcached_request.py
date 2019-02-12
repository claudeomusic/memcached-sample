class MemcachedRequest:
    """
    A request object class for our Memached server.
    """

    def __init__(self, request, db):
        self.args = request.recv(1024).strip().decode('utf-8').split(' ')
        self.db = db
        self.cache = {}

    @property
    def command(self):
        return self.args[0]

    @property
    def requires_additional_data(self):
        return self.command in ['set']

    def execute(self, followup=False):
        if followup:
            self.cache['data'] = self.args[0]
            return self.set_cache()

        options = {
            'set': self.prep_set_cache,
            'get': self.get_cache,
            'delete': self.delete_cache,
        }
        try:
            return options[self.command]()
        except KeyError:
            print('Invalid command.')
            return False

    def prep_set_cache(self):
        self.cache['key'] = self.args[1]
        self.cache['flags'] = self.args[2]
        return '\n'

    def set_cache(self):
        if self.db.insert_value(
                self.cache.get('key', ''), 
                self.cache.get('flags', ''), 
                self.cache.get('data', ''),
                ):
            return 'STORED\n'
        else:
            return 'EXISTS\n'

    def get_cache(self):
        key = self.args[1]
        flags, value = self.db.get_value(key)
        if flags and value:
            return 'VALUE %s %s %s\n%s\nEND\n' % (
              key, flags, len(value), value)

    def delete_cache(self):
        if self.db.delete_key(self.args[1]):
            return 'DELETED\n'
        else:
            return 'NOT_FOUND\n'
