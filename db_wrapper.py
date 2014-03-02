from util import DatabaseSingleton
import logger

import sqlite3
import os


class DBWrapper(metaclass=DatabaseSingleton):
    """
    Class to wrap an SQLite db.
    
    This class only defines useful methods for interacting with the
    database. Ways to use these methods must be defined elsewhere.

    name should be the database name excluding '.db'
    """
    
    def __init__(self, name, **args):
        # Create db filepath
        self.filepath = args.get('filepath', 'file') + os.path.sep
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

        self.name = name
        self.conn = sqlite3.connect(self.filepath + os.path.sep + name + '.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES)

        # Add converter for bool
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("bool", lambda v: bool(int(v)))

        # Logger
        self.log = logger.Logger()
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.log.log('Closing {} db.'.format(self.name))

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
        
        if one is None:
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
        
        if one is None:
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
                                 ' field names length!\n{}\n{}'.format(field_types, field_names))
        # Ensure that primary field is there
        elif False in [(x in field_names) for x in primary_name.split(', ')]:
            raise AssertionError('Primary name not in field names!')
        
        # Create statment
        stmt = ('CREATE TABLE {} ('
                '{}'
                'PRIMARY KEY ({}))')

        # Format the table name, field format spaces and primary name
        stmt = stmt.format(name,
                           '{} {},' * len(field_names),
                           primary_name)
        
        # Create symbols list for formatting
        symbols = []
        
        for i in range(len(field_names)):
            symbols += [field_names[i], field_types[i]]
        
        # Format the field names and types
        stmt = stmt.format(*symbols)

        self.log.log('Create statement: {}'.format(stmt))
        
        curs = self.conn.cursor()
        
        curs.execute(stmt)
        
        curs.close()
    
    def select_values(self, table, col_names, conditions):
        """
        Selects values from a table.
        Row_names is a list of strings that name a row in the table.
        Conditions is a list of strings already in the form of a valid
        SQL condition (e.g. "col_name = 100").
        """
        if conditions:
            cond_str = '{}' + ' AND {}' * (len(conditions) - 1)
            col_str = '{}' + ', {}' * (len(col_names) - 1)
            
            # Format table name and extra format strings
            stmt = ('SELECT {} '
                    'FROM {} '
                    'WHERE {}').format(col_str, table, cond_str)
            
            # Format the names and conditions into the new format strings
            stmt = stmt.format(*(col_names + conditions))
            
        else:
            col_str = '{}' + ', {}' * (len(col_names) - 1)
            
            # Format table name and condition format string
            stmt = ('SELECT {} '
                    'FROM {}').format(col_str, table)
            
            # Format conditions into format string
            stmt = stmt.format(*col_names)

        self.log.log('Select statement: {}'.format(stmt))
        
        # Get cursor and execute the statement
        curs = self.conn.cursor()
        curs.execute(stmt)
        
        # Return all results
        rows = curs.fetchall()
        curs.close()
        
        return rows
    
    def insert_values(self, table, values, ignore=False):
        """
        Inserts values into a table.
        
        Values is a list of tuples of the values for each row.
        """
        vals_str = ''
        for val in values:
            # Create and format the string for each set of values to
            # insert
            val_str = '(' + '{}' + ', {}' * (len(val) - 1) + ')'
            val_str = val_str.format(*val)
            
            # Append to list of sets of values
            vals_str += val_str + ', '
        
        vals_str = vals_str[:-2] # Drop the last ', '

        if ignore:
            stmt = ('INSERT OR IGNORE INTO {} '
                    'VALUES {}').format(table, vals_str)
        else:
            stmt = ('INSERT OR REPLACE INTO {} '
                    'VALUES {}').format(table, vals_str)
        
        self.log.log('Insert statement: {}'.format(stmt))
        
        # Execute the statement
        curs = self.conn.cursor()
        curs.execute(stmt)
        self.conn.commit()
        curs.close()

    def delete_values(self, table, conditions):
        """
        Deletes values from table using conditions
        """
        
        if conditions:
            cond_str = '{}' + ' AND {}' * (len(conditions) - 1)
            
            # Format table name and extra format strings
            stmt = ('DELETE FROM {} '
                    'WHERE {}').format(table, cond_str)
            
            # Format the conditions into the new format string
            stmt = stmt.format(*conditions)
            
        else:
            # Format table name format string
            stmt = 'DELETE FROM {}'.format(table)

        self.log.log('Delete statement: {}'.format(stmt))
        
        # Get cursor and execute the statement
        curs = self.conn.cursor()
        curs.execute(stmt)
        
        # Commit
        self.conn.commit()
