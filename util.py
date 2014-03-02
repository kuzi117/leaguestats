base_url = 'https://prod.api.pvp.net/api/lol/{}/v{}/' # region, v. num.
key = 'b327abf7-c1ef-4b97-acce-5528d97d1437'

class Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class DatabaseSingleton(type):
    """
    A form of singleton where the singleton is based on a defining attribute.
    In this case, which instance to return hinges on the database name.
    """
    instances = {}
    def __call__(cls, name, *args, **kw):
        if name not in cls.instances:
            cls.instances[name] = super(DatabaseSingleton, cls).__call__(name, *args, **kw)
        return cls.instances[name]