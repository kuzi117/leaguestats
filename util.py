# String constants
dbg_str = 'DEBUG: '
base_url = 'https://prod.api.pvp.net/api/lol/{}/v{}/' # region, v. num.
key = 'b327abf7-c1ef-4b97-acce-5528d97d1437'

class Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance
