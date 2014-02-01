from util import Singleton

import sqlite3

file_path = 'file'
dbg_str = 'DEBUG: '

class DBWrapper(metaclass=Singleton):
    """
    Class to wrap an SQLite db.
    
    This class only defines useful methods for interacting with the
    database. Ways to use these methods must be defined elsewhere.
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
        
        Doesn't do fancy injection prevention because table names can't
        be paramaterized.
        """
        # Ensure that all fields are typed
        if len(field_types) != len(field_names):
            raise AssertionError('Field types length doesn\'t match '
                                  ' field names length!')
        # Ensure that primary field is there
        elif primary_name not in field_names:
            raise AssertionError('Primary name not in field names!')
        
        # Create statment
        stmt = ('CREATE TABLE {} ('
                '{}'
                'PRIMARY KEY ({}))')
        
        # Format the table name, field format spaces and primary name
        stmt= stmt.format(name,
                          '{} {},' * len(field_names),
                          primary_name)
        
        # Create symbols list for formatting
        symbols = []
        
        for i in range(len(field_names)):
            symbols += [field_names[i], field_types[i]]
        
        # Format the field names and types
        stmt = stmt.format(*symbols)
        
        curs = self.conn.cursor()
        
        curs.execute(stmt)
        
        curs.close()
    
    
