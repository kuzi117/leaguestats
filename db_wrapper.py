import sqlite3

file_path = 'file'
dbg_str = 'DEBUG: '

class DBWrapper():
    """
    Class to wrap an SQLite db for stats storing.
    """
    
    def __init__(self, debug = False):
        self.debug = debug
        self.conn = sqlite3.connect(file_path + '/stats.db')
    
    def close(self):
        """
        Prepares for exit.
        """
        if self.debug:
            print(dbg_str + 'Closing stats db.')
        
        self.conn.close()
        
    def does_table_exist(self, table_name):
        """
        Returns whether or not a table exists in the database.
        """
        # Get DB cursor
        cursor = self.conn.cursor()
        
        # Prep the statement
        symbols = (table_name,)
        statement = ('SELECT name '
                     'FROM sqlite_master '
                     'WHERE type=\'table\' AND name=?;')
        
        # Get results
        cursor.execute(statement, symbols)
        one = cursor.fetchone()
        cursor.close()
        
        if one != None:
            return True
        else:
            return False
