class MemcachedRequest:
    """
    A request object class for our Memached server.
    """

    def __init__(self, request, db):
        self.update(request)
        self.db = db
        self.cache = {}

    @property
    def command(self):
        return self.args[0]

    @property
    def requires_additional_data(self):
        return self.command in ['set']

    def update(self, request):
        self.args = self._parse_request(request)

    def execute(self, followup=False):
        if followup:
            self.cache['data'] = self.args[0]
            return self._set_cache()

        options = {
            'set': self._prep_set_cache,
            'get': self._get_cache,
            'delete': self._delete_cache,
        }
        try:
            return options[self.command]()
        except KeyError:
            return 'ERROR\n'

    def _prep_set_cache(self):
        self.cache['key'] = self.args[1]
        self.cache['flags'] = self.args[2]
        return '\n'

    def _set_cache(self):
        key = self.cache.get('key', '')
        flags = self.cache.get('flags', '')
        data = self.cache.get('data', '')
        print('Executing set with key=%s, flags=%s, data=%s.' %
              (key, flags, data))
        if self.db.insert_value(key, flags, data):
            return 'STORED\n'
        else:
            return 'EXISTS\n'

    def _get_cache(self):
        key = self.args[1]
        print('Executing get with key=%s.' %
              (key))
        flags, value = self.db.get_value(key)
        if flags and value:
            return 'VALUE %s %s %s\n%s\nEND\n' % (
                key, flags, len(value), value)
        else:
            return 'ERROR\n'

    def _delete_cache(self):
        key = self.args[1]
        print('Executing delete with key=%s.' %
              (key))
        if self.db.delete_key(self.args[1]):
            return 'DELETED\n'
        else:
            return 'NOT_FOUND\n'

    def _parse_request(self, request):
        return request.recv(1024).strip().decode('utf-8').split(' ')
