from util import Singleton, dbg_str
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
    
    def summoner_by_name(self, name, region):
        """
        Gets a summoner by name from the database. Returns only a single
        summoner.
        """
        name = name.lower().replace(' ', '')
        rows = self.db.select_values('summoners',
                                     ['*'],
                                     ['standard_name like \'{}\''
                                     .format(name)])
        if rows:
            # Drop the cache date and standardized name from the end of 
            # the result so it's like riot's result
            rows = [
                {'id': x[0],
                 'name': x[1],
                 'summonerLevel': x[2],
                 'profileIconId': x[3],
                 'revisionDate': x[4]
                    }
                     for x in rows]
                     
            if self.debug:
                print(dbg_str + 'Summoners from db: {}'.format(rows))
            
            return rows[0]
        else:
            return None
    
    ### Save functions
    def save_summoners(self, summoners):
        """
        Saves summoners to the database. 
        Expects summoners to be a list of SummonerDto.
        """
        values = []
        for summoner in summoners:
            val_list = []
            
            # Append all values in order.
            val_list.append(summoner['id'])
            val_list.append('\'{}\''.format(summoner['name']))
            val_list.append(summoner['summonerLevel'])
            val_list.append(summoner['profileIconId'])
            val_list.append(summoner['revisionDate'])
                            
            # Add cache date and standardized name
            val_list.append('\'{}\''.format(summoner['name']
                                .lower().replace(' ', '')))
            val_list.append('datetime(\'now\')')
            
            values.append(tuple(val_list))
        
        self.db.insert_values('summoners', values)
        
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
                 'standard_name',
                 'cacheDate')
        types = ('integer',
                 'text',
                 'integer',
                 'integer',
                 'integer',
                 'text',
                 'integer')
        
        self.db.create_table('summoners', names, types, 'id')
