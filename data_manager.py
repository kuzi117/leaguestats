from util import Singleton, dbg_str
import db_wrapper

import datetime

class DataManager(metaclass=Singleton):
    """
    Class to manage data like summoners, recent games, etc.
    """
    def __init__(self, **args):
        self.debug = args.get('debug', False)
        
        # Database handle
        self.stat_db = db_wrapper.DBWrapper('stats',
                                            debug = self.debug)
        
        # How long should we cache for?
        self.summoner_expire_sec = 60 # 1 day
        
        if not self.stat_db.table_exists('summoners'):
            self.setup_summoners()
        elif self.debug:
            print(dbg_str + 'Summoners table already setup.')
            self.prune_summoners()
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.stat_db.exit()

    ### Get functions
    def summoners_by_name(self, names, region):
        """
        Gets summoners by list of standardized names from the database. Returns as many
        summoners as can be found.
        """
        # Create format string for names and format the names into it
        name_str = '(' + '\'{}\'' + (', \'{}\'' * (len(names)-1)) + ')'
        name_str = name_str.format(*names)

        rows = self.stat_db.select_values('summoners',
                                          ['*'],
                                          ['standardName in {}'
                                          .format(name_str)])

        if rows:
            # Drop the cache date and standardized name from the end of 
            # the result so it's like riot's result
            rows = {x[1]:
                    {'id': x[0],
                    'name': x[1],
                    'summonerLevel': x[2],
                    'profileIconId': x[3],
                    'revisionDate': x[4]
                    } for x in rows}
                     
            if self.debug:
                print(dbg_str + 'Summoners from db: {}'.format(rows))
            
            return rows
        else:
            return None

    def summoner_by_name(self, name, region):
        """
        Gets a summoner by name. Delegates to summoners_by_name.
        Returns the same way as summoner by name.
        """
        return self.summoners_by_name([name], region)

    ### Save functions
    def save_summoners(self, summoners, region):
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
                            
            # Add region, cache date and standardized name
            val_list.append('\'{}\''.format(region))
            val_list.append('\'{}\''.format(summoner['name']
                                .lower().replace(' ', '')))
            val_list.append('datetime(\'now\')')
            
            values.append(tuple(val_list))
        
        self.stat_db.insert_values('summoners', values)
        
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
                 'region',
                 'standardName',
                 'cacheDate')
        types = ('integer',
                 'text',
                 'integer',
                 'integer',
                 'integer',
                 'text',
                 'text',
                 'integer')
        
        self.stat_db.create_table('summoners', names, types, 'id, region')
    
    ### Clean up functions
    def prune_summoners(self):
        """
        Cleans up the summoners table by removing old entries older than
        a supplied time.
        """
        # Select all summoners
        rows = self.stat_db.select_values('summoners',
                                          ['standardName', 'cacheDate'],
                                          [])
        
        # If nothing to prune, quit
        if not rows:
            return
        
        # Convert second string to date
        rows = [(name, datetime.datetime.strptime(dt_str, 
                                                  '%Y-%m-%d %H:%M:%S'))
                for (name, dt_str) in rows]
        
        now = datetime.datetime.now()
        remove = []
        for name, date in rows:
            if (now - date).total_seconds() > self.summoner_expire_sec:
                remove.append(name)
        
        if not remove:
            return
        elif len(remove) == 1:
            self.stat_db.delete_values('summoners',
                                       ['standardName in {}'
                                        .format('\'{}\''.format(remove[0]))
                                       ])
        else:
            self.stat_db.delete_values('summoners',
                                       ['standardName in {}'
                                        .format(tuple(remove))
                                       ])
        
        
