import db_wrapper

dbg_str = 'DEBUG: '

class StatManager():
    def __init__(self, debug = False):
        self.debug = debug
        
        self.db = db_wrapper.DBWrapper(debug = debug)
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.db.close()
