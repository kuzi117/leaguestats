import sqlite3

file_path = 'file'
dbg_str = 'DEBUG: '

class DBWrapper():
    """
    Class to wrap an SQLite db for stats storing.
    """
    
    def __init__(self, **args):
        self.debug = args.get('debug', False)
        self.conn = sqlite3.connect(file_path + '/stats.db')
    
    def exit(self):
        """
        Prepares for exit.
        """
        if self.debug:
            print(dbg_str + 'Closing stats db.')
        
        self.conn.close()
        
    def table_exists(self, table_name):
        """
        Returns whether or not a table exists in the database.
        """
        # Prep the statement and symbols
        stmt = ('SELECT name '
                'FROM sqlite_master '
                'WHERE type=\'table\' AND name=?;')
        symbols = (table_name,)
        
        # Get DB cursor
        cursor = self.conn.cursor()
        
        # Get results
        cursor.execute(stmt, symbols)
        one = cursor.fetchone()
        cursor.close()
        
        if one != None:
            return True
        else:
            return False
    
    def row_exists(self, table_name, row_name):
        """
        Returns whether or not a row exists in a table.
        """
        # Prep statement and symbols
        stmt = ('SELECT ? '
                'FROM ? ')
        symbols = (table_name, row_name)
        
        # Get DB cursor
        cursor = self.conn.cursor()
        
        # Get results
        cursor.execute(stmt, symbols)
        one = cursor.fetchone()
        cursor.close()
        
        if one != None:
            return True
        else:
            return False
        

    def create_table(self, name, field_names, field_types, primary_name):
        """
        Creates a table.
        """
        # Ensure that all fields are typed
        if len(field_types) != len(field_names):
            raise AssertionError('Field types length doesn\'t match '
                                  ' field names length!')
        # Ensure that primary field is there
        elif primary_name not in field_names:
            raise AssertionError('Primary name not in field names!')
        
        # Create statment
        stmt = ('CREATE TABLE ? ('
                '{}'
                'PRIMARY KEY (?))')
        stmt= stmt.format('? ?,' * len(field_names))
        
        # Create symbols list for formatting
        symbols = [name]
        
        for i in range(len(field_names)):
            symbols += [field_types[i]]
            symbols += [field_names[i]]
        
        symbols += [primary_name]
        
        curs = self.conn.cursor()
        
        curs.execute(stmt, symbols)
        
        curs.close()
    
