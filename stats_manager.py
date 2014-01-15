import db_wrapper

dbg_str = 'DEBUG: '

class StatsManager():
    def __init__(self, debug = False):
        self.debug = debug
        
        self.db = db_wrapper.DBWrapper(debug = debug)
    
    def update_aram_percents():
        pass
    
    def close(self):
        """
        Prepares for exit.
        """
        self.db.close()
