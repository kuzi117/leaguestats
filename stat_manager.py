import db_wrapper
from util import dbg_str

class StatManager():
    def __init__(self, debug = False):
        self.debug = debug
        
        self.db = db_wrapper.DBWrapper(debug = debug)
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.db.exit()
