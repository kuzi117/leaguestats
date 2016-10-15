import threading

base_url = 'https://{}.api.pvp.net/api/lol/{}/v{}/' # region, region, v. num.
key = '33bbdc99-d0ee-426a-ba0f-21297aeee69e'

class Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class KeySingleton(type):
    """
    A form of singleton where the singleton is based on a defining attribute.
    Only one instance for each defining attribute and class combination will be created.
    """
    instances = {}
    def __call__(cls, key, *args, **kw):
        if cls.__name__ not in cls.instances:
            cls.instances[cls.__name__] = {key: super(KeySingleton, cls).__call__(*args, **kw)}
        elif key not in cls.instances[cls.__name__]:
            cls.instances[cls.__name__][key] = super(KeySingleton, cls).__call__(*args, **kw)
        return cls.instances[cls.__name__][key]


class DatabaseSingleton(KeySingleton):
    """
    KeySingleton where key is database name and the current thread ident.
    """
    def __call__(cls, name, *args, **kw):
        return KeySingleton.__call__(cls, (name, threading.get_ident()), name, *args, **kw)

class ThreadSingleton(KeySingleton):
    """
    KeySingleton where key is current thread ident.
    """
    def __call__(cls, *args, **kw):
        return KeySingleton.__call__(cls, threading.get_ident(), *args, **kw)
