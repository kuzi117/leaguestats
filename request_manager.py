import api_wrapper as api
import data_manager as data
from util import Singleton, dbg_str, wrn_str

class RequestManager(metaclass=Singleton):
    def __init__(self, **args):
        # Default things
        self.debug = args.get('debug', False)
        
        # Wrappers to request from
        self.apiw = api.APIWrapper(debug = self.debug)
        self.datam = data.DataManager(debug = self.debug)
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.datam.exit()
    
    def summoner_by_name(self, name, region):
        """
        Request a summoner by name.
        
        Checks with the data manager before requesting from the server.
        """
        # Make sure summoner name is acceptable
        if name in [None, ''] or type(name) != str:
            if self.debug:
               print(dbg_str + 'Bad summoner name.')
            return None
        
        summoner = self.datam.summoner_by_name(name, region)
        
        # If the summoner was cached locally then return it
        if summoner: return summoner
        
        # Request from server
        summoners = self.apiw.summoner_by_name(name, region)
        
        if summoners:
            # Convert to a list the dict is useless here
            summoners = [summoners[x] for x in summoners]
            
            # Save the results of the server request
            self.datam.save_summoners(summoners, region)
            
            if self.debug and len(summoners) > 1:
                print(wrn_str + 'More than one summoner returned on '
                        'single request!')
            
            return summoners.pop() # Return first in list
        
        else:
            return None
    
    def recent_games(self, sumid, region):
        return self.apiw.recent_games(sumid, region)
    
        
