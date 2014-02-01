from util import dbg_str
from util import base_url
from util import key
from util import Singleton

import requests as reqs

GENERIC_ERROR = 0
NOT_FOUND = 1
CLIENT_ERROR = 2
SERVER_ERROR = 3

def _get(region, version, url, payload={}, **args):
    """
    Generic get from Riot.
    
    Returns an error code or the recieved object already converted to
    usable form.
    """
    url = base_url.format(region, version) + url
    
    # Print URL if debug is on
    if args.get('debug', False):
        print(dbg_str + 'REQUEST URL: ' + url)
    payload['api_key'] = key

    # Request
    r = reqs.get(url, params = payload)
    
    if args.get('debug', False):
        print(dbg_str + 'RESPONSE STATUS CODE: {}'.format(r.status_code))
    
    # All good
    if r.status_code == 200:
        return r.json()
        
    # Error codes
    elif r.status_code == 400:
        if args.get('debug', False):
            print(dbg_str + 'Internal error; bad request generated!')
        return CLIENT_ERROR
    
    elif r.status_code == 401:
        if args.get('debug', False):
            print(dbg_str + 'Unauthorized request; bad key?')
        return CLIENT_ERROR
        
    elif r.status_code == 404:
        if args.get('debug', False):
            print(dbg_str + '{} not found on server!'
                .format(args.get('not_found', 'Requested object')))
        return NOT_FOUND
        
    elif r.status_code == 429:
        if args.get('debug', False):
            print(dbg_str + 'Too many requests!')
        return GENERIC_ERROR
    
    elif r.status_code == 500:
        if args.get('debug', False):
            print(dbg_str + 'Server error; generic error response!')
        return SERVER_ERROR
    
    elif r.status_code == 503:
        if args.get('debug', False):
            print(dbg_str + 'Server error; service unavailable!')
        return SERVER_ERROR
    
    else:
        if args.get('debug', False):
            print(dbg_str + 'UNKNOWN STATUS CODE {} RETURNED!'
                    .format(r.status_code))
        return GENERIC_ERROR

class APIWrapper(metaclass=Singleton):
    """
    A wrapper for Riot's developer API.
    """
    
    def __init__(self, **args):
        # Default things
        self.debug = args.get('debug', False)
    
    def sum_by_name(self, name, region):
        """
        Returns summoner object by name, or None if the couldn't be
        found or if another error occurs.
        """
        if name == None or type(name) != str:
            if self.debug:
               print(dbg_str + 'Bad summoner name.')
            return None
        
        result = _get(region, 1.3, 'summoner/by-name/{}'.format(name),
                        debug = self.debug)
        
        if result == NOT_FOUND:
            print('That name couldn\'nt be found on this server.')
            return None
        elif result == CLIENT_ERROR:
            print('There was a client error requesting the summoner.')
            return None
        elif result == SERVER_ERROR:
            print('There was a server error requesting the summoner. '
                   'Try again later?')
            return None
        elif result == GENERIC_ERROR:
            print('An unkown error occured. Try again later?')
            return None
        else:
            return result
            
    def recent_games(self, sumid, region):
        """
        Gets recent games by summoner id.
        """
        # Make sure summoner id
        if sumid == None or type(sumid) != int:
            return None
        
        result = _get(1.3, 'game/by-summoner/{}/recent'.format(sumid))
        
        if result == NOT_FOUND:
            print('That name couldn\'nt be found on this server.')
            return None
        elif result == CLIENT_ERROR:
            print('There was a client error requesting recent games.')
            return None
        elif result == SERVER_ERROR:
            print('There was a server error requesting recent games. '
                   'Try again later?')
            return None
        elif result == GENERIC_ERROR:
            print('An unkown error occured. Try again later?')
            return None
        else:
            return result
