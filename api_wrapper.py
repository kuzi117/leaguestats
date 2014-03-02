from util import base_url, key, Singleton
import logger

import requests as reqs

GENERIC_ERROR = 0
NOT_FOUND = 1
CLIENT_ERROR = 2
SERVER_ERROR = 3

def _get(region, version, url, payload={}):
    """
    Generic get from Riot.
    
    Returns an error code or the received object already converted to
    usable form.
    """
    # Logger
    log = logger.Logger()

    url = base_url.format(region, version) + url
    
    # Print URL if debug is on
    log.log('REQUEST URL: ' + url)
    payload['api_key'] = key

    # Request
    r = reqs.get(url, params=payload)
    
    log.log('RESPONSE STATUS CODE: {}'.format(r.status_code))
    
    # All good
    if r.status_code == 200:
        return r.json()
        
    # Error codes
    elif r.status_code == 400:
        log.log('Internal error; bad request generated!')
        return CLIENT_ERROR
    
    elif r.status_code == 401:
        log.log('Unauthorized request; bad key?')
        return CLIENT_ERROR
        
    elif r.status_code == 404:
        log.log('Requested object not found on server!')
        return NOT_FOUND
        
    elif r.status_code == 429:
        log.log('Too many requests!')
        return GENERIC_ERROR
    
    elif r.status_code == 500:
        log.log('Server error; generic error response!')
        return SERVER_ERROR
    
    elif r.status_code == 503:
        log.log('Server error; service unavailable!')
        return SERVER_ERROR
    
    else:
        log.log('UNKNOWN STATUS CODE {} RETURNED!'.format(r.status_code))
        return GENERIC_ERROR

class APIWrapper(metaclass=Singleton):
    """
    A wrapper for Riot's developer API.
    """
    
    def __init__(self):
        # Logger
        self.log = logger.Logger()
    
    def summoners_by_name(self, names, region):
        """
        Gets multiple summoners specified by list of names

        Returns a Dict with summoner info in it.
        """
        # Create format string for names and format the names into it
        name_str = "{}" + (",{}" * (len(names)-1))
        name_str = name_str.format(*names)

        result = _get(region, 1.3, 'summoner/by-name/{}'.format(name_str))

        if result in [NOT_FOUND, CLIENT_ERROR, SERVER_ERROR, GENERIC_ERROR]:
            return None
        else:
            self.log.log('Summoners from server: {}'.format([name for name in result]))

            return result
            
    def recent_games(self, id, region):
        """
        Gets recent games by summoner id.
        """
        # Make sure summoner id
        if id is None or type(id) != int:
            return None
        
        result = _get(region, 1.3, 'game/by-summoner/{}/recent'.format(id))
        
        if result == NOT_FOUND:
            print('That name couldn\'t be found on this server.')
            return None
        elif result == CLIENT_ERROR:
            print('There was a client error requesting recent games.')
            return None
        elif result == SERVER_ERROR:
            print('There was a server error requesting recent games. Try again later?')
            return None
        elif result == GENERIC_ERROR:
            print('An unknown error occurred. Try again later?')
            return None
        else:
            # Return only the list of games
            return result['games']
