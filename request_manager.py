import api_wrapper as api
import file_wrapper as files
import data_manager as data
from util import Singleton

class RequestManager(metaclass=Singleton):
    def __init__(self, **args):
        # Default things
        self.debug = args.get('debug', False)
        
        # Wrappers to request from
        self.apiw = api.APIWrapper(debug = self.debug)
        self.filew = files.FileWrapper(debug = self.debug)
        self.datam = data.DataManager(debug = self.debug)
    
    def exit(self):
        """
        Prepares for exit.
        """
        self.filew.exit()
        self.datam.exit()
    
    def sum_by_name(self, name, region):
        return self.apiw.sum_by_name(name, region)
    
    def recent_games(self, sumid, region):
        return self.apiw.recent_games(sumid, region)
    
        
