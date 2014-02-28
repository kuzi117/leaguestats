from util import Singleton, dbg_str
import db_wrapper
import stat_list

import datetime
import copy

class DataManager(metaclass=Singleton):
    """
    Class to manage data like summoners, recent games, etc.
    """
    def __init__(self, **args):
        self.debug = args.get('debug', False)
        
        # Database handle
        self.stat_db = db_wrapper.DBWrapper('stats',
                                            debug = self.debug)

        self.recent_db = db_wrapper.DBWrapper('recent',
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
        self.recent_db.exit()

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
            rows = {x[6]:
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

    def save_recent_games(self, id, region, games):
        """
        Saves recent games for a summoner
        """
        if not self.recent_db.table_exists('{}_{}'.format(region, id)):
            self.setup_recents(id, region)

        if self.debug:
            print(dbg_str + 'Saving recent games for {}_{}'.format(region, id))

        # Must deep copy games, else popping things destroys the original
        games = copy.deepcopy(games)

        games = []
        for game in games:
            games.append((game,
                          game.pop('fellowPlayers') if 'fellowPlayers' in game else {},
                          game.pop('stats')))

        # Default values for fields
        default_vals = {'text':'',
                        'bool': False,
                        'integer': 0}

        values = []
        for game in games:
            val_list = []

            # Do base stats
            names, types = stat_list.base_db_fields()
            for i in range(len(names)):
                # We have a value for this stat
                if names[i] in game[0]:
                    val_list.append(game[0][names[i]])
                # Need a default value
                else:
                    # Default value for type
                    val_list.append(default_vals[types[i]])

            # This is an ugly solution, but it works.. for now
            names, types = stat_list.fellow_player_db_fields()
            for player in sorted(game[1], key = lambda x: x['teamId']):
                if len(player) != 3:
                    raise AssertionError('Fellow player was only {} long!'.format(len(player)))
                val_list.append(player['championId'])
                val_list.append(player['summonerId'])
                val_list.append(player['teamId'])

            # Add in missing players
            for i in range(int((len(names)/3) - len(game[1]))):
                val_list.append(None)
                val_list.append(None)
                val_list.append(None)


            # Do base stats
            names, types = stat_list.stats_db_fields(prefix=False)
            for i in range(len(names)):
                # We have a value for this stat
                if names[i] in game[2]:
                    val_list.append(game[2][names[i]])
                # Need a default value
                else:
                    # Default value for type
                    val_list.append(default_vals[types[i]])

            # Convert all values into values acceptable by db
            for i in range(len(val_list)):
                if type(val_list[i]) == str:
                    val_list[i] = '\'{}\''.format(val_list[i])
                if type(val_list[i]) == bool:
                    val_list[i] = int(val_list[i])
                if val_list[i] == None:
                    val_list[i] = 'null'



            values.append(val_list)


        self.recent_db.insert_values('{}_{}'.format(region, id), values, ignore=True)


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

    def setup_recents(self, id, region):
        """
        Sets up the the table that holds recent games for a certain summoner in a region
        """
        if self.debug:
            print(dbg_str + 'Setting up recent table for \'{}_{}\''.format(region, id))

        names, types = stat_list.game_db_fields()
        self.recent_db.create_table('{}_{}'.format(region, id),
                                    names,
                                    types,
                                    stat_list.primary_key)

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
        else:
            # Generate csv of names
            rm_str = '\'{}\'' + ', \'{}\'' * (len(remove)-1)
            rm_str = rm_str.format(*remove)

            # format rm_str into the condition statement
            self.stat_db.delete_values('summoners',
                                       ['standardName in ({})'
                                        .format(rm_str)
                                       ])
        
        
