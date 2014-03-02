import db_wrapper

class StatManager():
    def __init__(self, debug = False):
        self.debug = debug
        
        self.db = db_wrapper.DBWrapper('stats', debug = debug)
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.db.exit()
