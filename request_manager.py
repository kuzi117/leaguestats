import api_wrapper as api
import data_manager as data
from util import ThreadSingleton
import logger

import copy


class RequestManager(metaclass=ThreadSingleton):
    def __init__(self):
        # Wrappers to request from
        self.apiw = api.APIWrapper()
        self.datam = data.DataManager()

        # Logger
        self.log = logger.Logger()

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
        # copy the list so we don't affect it
        names = copy.copy(names)

        # Make sure all summoner names are acceptable
        if (True in [(name in [None, '']) for name in names] or
                    True in [(type(name) != str) for name in names] or
                    False in [(name.islower() and name.count(' ') == 0) for name in names]):
            self.log.log('Bad summoner name. {}'.format(names))
            return None

        summoners = self.datam.summoners_by_name(names, region)

        # If we didn't find anything move on
        if summoners:
            remove = []
            # If we already found a summoner remove them from the need to find list
            for name in names:
                if name in summoners:
                    remove.append(name)

            for rem in remove:
                names.remove(rem)

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

    def recent_games(self, id, region, n=10):
        """
        Gets recent games for a summoner.

        Returns n games if possible. If less games than requested are found then as many games as possible will be
        returned.
        """
        games = self.apiw.recent_games(id, region)

        # Save the games
        self.datam.save_recent_games(id, region, games)

        if n <= 10:
            return games[:n]
        # This is where adding games from the db will happen
        else:
            return games
