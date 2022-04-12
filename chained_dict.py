class ChainedDict(object):
    def __init__(self):
        self.dicts = []

    def get(self, key):
        for c in reversed(self.dicts):
            if key in c:
                return c[key]
        raise KeyError(str(key))
            

    def set(self, key, value):
        for c in reversed(self.dicts):
            if key in c:
                c[key] = value
                return
        raise KeyError(str(key))

    def insert(self, key, value):
        if key in self.dicts[-1]:
            raise Exception(f"{str(key)} in dict")
        self.dicts[-1][key] = value
        return True

    def push(self):
        self.dicts.append({})

    def pop(self):
        self.dicts.pop()

    def __contains__(self, key):
        for c in self.dicts:
            if key in c:
                return True
        return False

    def __str__(self):
        return str(self.dicts)
        