


class ResourceManager(object):
    def __init__(self, resource_class, api_handler):
        self.resource_class = resource_class
        self.api_handler = api_handler

    def __call__(self, **kwargs):
        return self.resource_class(handler=self.api_handler, **kwargs)

    def find(self, object_id):
        return self.resource_class.find(self.api_handler, object_id)

    def findOrCreate(self, data):
        return self.resource_class.findOrCreate(self.api_handler, data)

    def search(self, args = None):
        return self.resource_class.search(self.api_handler, args)

    def findWhere(self, args):
        return self.resource_class.findWhere(self.api_handler, args)

    def all(self, args = None):
        return self.resource_class.all(self.api_handler, args = args)

    def save(self):
        return self.resource_class.save(self.api_handler)

    def delete(self):
        return self.resource_class.delete(self.api_handler)

class UserResourceManager(ResourceManager):
    def me(self):
        return self.resource_class.me(self.api_handler)

class CartResourceManager(ResourceManager):
    def mine(self):
        return self.resource_class.mine(self.api_handler)
