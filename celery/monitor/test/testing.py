class A:
    @property
    def name(self):
        return self.name
    def set(self, name):
        self.name = name

class B:
    @classmethod
    def name(self):
        return self.name
    @classmethod
    def set(self, name):
        self.name = name

class B:
    @classmethod
    def setname(self):
        return self.name

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('/%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    def user(self, name):
        self._path = name
        return self

print dir(A)