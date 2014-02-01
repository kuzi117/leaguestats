from util import Singleton
from util import dbg_str
import db_wrapper

class DataManager(metaclass=Singleton):
    """
    Class to manage data like summoners, recent games, etc.
    """
    def __init__(self, **args):
        self.debug = args.get('debug', False)
        
        # Database handle
        self.db = db_wrapper.DBWrapper(debug = self.debug)
        
        if not self.db.table_exists('summoners'):
            self.setup_summoners()
        elif self.debug:
            print(dbg_str + 'Summoners table already setup.')
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.db.exit()
    
    def sum_by_name(self, name, region):
        """
        Gets a summoner by name from the database.
        """
        pass
        
    ### Setup functions
    def setup_summoners(self):
        """
        Sets up the table that holds summoner info.
        """
        if self.debug:
            print(dbg_str + 'Setting up summoners table.')
        
        names = ('id',
                 'name',
                 'summonerLevel',
                 'profileIconId',
                 'revisionDate',
                 'cacheDate')
        types = ('integer',
                 'text',
                 'integer',
                 'integer',
                 'integer',
                 'integer')
        
        self.db.create_table('summoners', names, types, 'id')
