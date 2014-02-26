import api_wrapper as api
import data_manager as data
from util import Singleton, dbg_str, wrn_str


class RequestManager(metaclass = Singleton):
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

    def summoners_by_name(self, names, region):
        """
        Requests summoners by name.
        
        Checks with the data manager before requesting from the server.

        Returns as many as possible, both from local and server.
        If none found or a bad name is input None is returned
        """
        # Make sure all summoner names are acceptable
        if (True in [(name in [None, '']) for name in names] or
                    True in [(type(name) != str) for name in names] or
                    False in [(name.islower() and name.count(' ') == 0) for name in names]):
            if self.debug:
                print(dbg_str + 'Bad summoner name. {}'.format(names))
            return None

        summoners = self.datam.summoners_by_name(names, region)

        # If we already found a summoner remove them from the need to find list
        for name in names:
            if name in summoners:
                names.remove(name)

        # If names left to find then request from server
        if names:
            api_summoners = self.apiw.summoners_by_name(names, region)

            # Not much we can do if we find anything
            if api_summoners:

                # Save the results of the server request
                self.datam.save_summoners([api_summoners[x] for x in api_summoners],
                                          region)

                # Add the api results to the local results
                if summoners:
                    summoners.update(api_summoners)
                # Api results are only results
                else:
                    summoners = api_summoners

        if not summoners:
            return None

        return summoners

    def recent_games(self, sumid, region):
        return self.apiw.recent_games(sumid, region)
    
        
