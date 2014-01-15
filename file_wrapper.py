import json
import datetime
import copy
import os

class FileWrapper:
    """
    Implements useful functions for saving league of legends info.

    This wrapper is intended as a singleton, but does not guarantee it.
    """
    def __init__(self, debug = False):
        # Create folder if it doesn't exist
        if not os.path.exists('json/'):
            os.mkdir('json')
        
        # Refresh times (how long before cache is invalid)
        self.summoner_valid_seconds = 24*60*60 # 1 day
        self.games_valid_seconds = 30*60 # Half hour
        
        # Saved values
        self._summoners = _load_summoners(self.summoner_valid_seconds)
        self._games = _load_recent_games(self.games_valid_seconds,
                                         self._summoners)
    
    def close(self):
        """
        Implements shutdown and saving of all info.
        """
        _save_summoners(self._summoners)
        _save_recent_games(self._games)
    
    def get_summoner_by_name(self, name):
        """
        Gets summoner info by name.
        """
        if self._summoners == None:
            raise AssertionError('Summoners weren\'t loaded!')
        
        # Iterate over saved summoners
        for sumid in self._summoners:
            if (self._summoners[sumid]['name'].lower().replace(' ', '')
                == name.lower().replace(' ', '')):
                    # Deep copy the dict, don't want the saved date deleted
                    summoner = copy.deepcopy(self._summoners[sumid])
                    
                    # Remove saved date
                    del summoner['saved']
                    
                    # Re-add the summoner id, now dict is identical to what
                    # would come from servers
                    summoner['id'] = sumid
                    
                    return summoner
        
        # Return None if couldn't be found
        return None
    
    def get_summoner_by_id(self, sumid):
        """
        Gets summoner info by id.
        """
        if self._summoners == None:
            raise AssertionError('Summoners weren\'t loaded!')
        
        if sumid not in self._summoners:
            return None
        
        summoner = copy.deepcopy(self._summoners[sumid])
        
        # Reformat to Riot format
        summoner['id'] = sumid
        del summoner['saved']
        
        return summoner
    
    def get_recent_games(self, sumid):
        """
        Gets recent games by summoner id.
        """
        if self._games == None:
            raise AssertionError('Games weren\'t loaded!')
        
        if sumid not in self._games:
            return None
        
        games = copy.deepcopy(self._games[sumid])
        
        # Reformat to Riot format
        games['summonerId'] = sumid
        del games['saved']
        
        return games
        
    def save_summoner(self, orig_summoner):
        # Copy the other version so we can modify this one
        summoner = copy.deepcopy(orig_summoner)
        
        # Add the saved date
        now = datetime.datetime.now()
        summoner['saved'] = [now.year, now.month, now.day, now.hour,
                             now.minute, now.second]
        
        # Pop summoner id for index in saving
        sumid = summoner.pop('id')
        self._summoners[sumid] = summoner
    
    def save_recent_games(self, orig_games):
        games = copy.deepcopy(orig_games)
        
        # Add the saved date
        now = datetime.datetime.now()
        games['saved'] = [now.year, now.month, now.day, now.hour,
                             now.minute, now.second]
        
        # Pop summoner id for index in saving
        sumid = games.pop('summonerId')
        self._games[sumid] = games
        
def _load_summoners(summoner_valid_seconds, debug=False):
    # If no file there's nothing to load
    if not os.path.exists('json/summoners.json'):
        return {}
    
    # Open the file and read with json lib
    with open('json/summoners.json', 'r') as sum_file:
        loaded_sums = json.load(sum_file)
    
    # Prune old entries
    now = datetime.datetime.now()
    removes = []
    for sumid in loaded_sums:
        saved = loaded_sums[sumid]['saved']
        saved = datetime.datetime(saved[0], saved[1], saved[2], saved[3],
                                  saved[4], saved[5])
        delta = now - saved 
        # Remove if difference > allowed
        if delta.days > summoner_valid_seconds:
            
            # Notify if debug is on
            if debug:
                print('PRUNING ID {}({}) FROM SAVED SUMMONERS'
                       .format(sumid, loaded_sums[sumid]['name']))
            
            # Remove the summoner
            removes.append(sumid)
    
    # Delete outdated
    for sumid in removes:
        del loaded_sums[sumid]
    
    # Convert keys back to int
    saved_sums = {}
    for sumid in loaded_sums:
        saved_sums[int(sumid)] = loaded_sums[sumid]
    del loaded_sums
    
    return saved_sums

def _save_summoners(summoners):
    # Truncate the original file
    with open('json/summoners.json', 'w') as sum_file:
        json.dump(summoners, sum_file)

def _load_recent_games(games_valid_seconds, sums, debug=False):
        # If no file there's nothing to load
    if not os.path.exists('json/recent_games.json'):
        return {}
    
    # Open the file and read with json lib
    with open('json/recent_games.json', 'r') as game_file:
        loaded_recents = json.load(game_file)
    
    # Prune old entries
    now = datetime.datetime.now()
    removes = []
    for sumid in loaded_recents:
        saved = loaded_recents[sumid]['saved']
        saved = datetime.datetime(saved[0], saved[1], saved[2], saved[3],
                                  saved[4], saved[5])
        delta = now - saved 
        # Remove if difference > allowed
        if delta.total_seconds() > games_valid_seconds:
            
            # Notify if debug is on
            if debug:
                print('PRUNING ID {}({}) FROM SAVED SUMS'
                       .format(sumid, sums[sumid]['name']))
            
            # Save the id for deletion
            removes.append(sumid)
    
    # Delete outdated
    for sumid in removes:
        del loaded_recents[sumid]
    
    # Convert keys back to int
    saved_recents = {}
    for sumid in loaded_recents:
        saved_recents[int(sumid)] = loaded_recents[sumid]
    
    del loaded_recents
    
    return saved_recents

def _save_recent_games(games):
    # Truncate the original file
    with open('json/recent_games.json', 'w') as game_file:
        json.dump(games, game_file)
