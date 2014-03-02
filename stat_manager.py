import db_wrapper

class StatManager():
    def __init__(self):
        
        self.db = db_wrapper.DBWrapper('stats')
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.db.exit()
