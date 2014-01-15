import file_wrapper

import requests as reqs

import datetime
from time import sleep

# Application varaibles
debug = False
dbg_str = 'DEBUG: '
files = file_wrapper.FileWrapper(debug = debug)
request_queue = []

# Riot API variables
key = 'b327abf7-c1ef-4b97-acce-5528d97d1437'
base_url = 'https://prod.api.pvp.net/api/lol/na/v{}/'

def _get(version, url, payload = {}):
    """
    Generic get from Riot.
    """
    # Clean the queue out
    now = datetime.datetime.now()
    while (len(request_queue) > 0 and
            (now-request_queue[0]).total_seconds() > 10):
        request_queue.pop(0)
    
    # Sleep for the remainder of the ten seconds on the earliest request
    if len(request_queue) >= 10:
        wait = 10-(now-request_queue[0]).total_seconds()
        if debug:
            print(dgb_str + 'WAITING ON NEXT AVAILABLE REQUEST ({}s)'
                    .format(wait))
        sleep(wait)
        request_queue.pop(0)
        
    url = base_url.format(version) + url
    
    # Print URL if debug is on
    if debug:
        print(dbg_str + 'REQUEST URL: ' + url)
    
    payload['api_key'] = key
    
    # Request
    request_queue.append(datetime.datetime.now())
    r = reqs.get(url, params = payload)
    
    if debug:
        print(dbg_str + 'RESPONSE STATUS CODE: {}'.format(r.status_code))
    
    # All good
    if r.status_code == 200:
        return r
    # Error code
    else:
        if debug and r.status_code == 429:
            print(dbg_str + "TOO MANY REQUESTS!")
        return r.status_code

def get_summoner_by_name(name, force_reload=False):
    # Ensure name entered wasn't empty
    if name == None:
        return
    
    # Request locally
    file_result = files.get_summoner_by_name(name)
    if file_result != None and not force_reload:
        if debug:
            print(dbg_str + 'FOUND SUMMONER IN LOCAL CACHE')
            
        return file_result
    
    result = _get(1.2, 'summoner/by-name/{}'.format(name))
    
    # Notify user on HTTP error codes
    if type(result) == int:
        if result == 404:
            print('That name couldn\'nt be found on this server.')
        elif result == 400:
            print('An internal error occured while contacting '
                   'the server!')
        elif result == 500:
            print('Servers are experiencing difficulties, try again.')
        else:
            print('An unknown error occured! ({})'.format(result))
        
        # All of these return no user found
        return None
    else:
        # Convert from json format to dict
        result = result.json()
        
        # Save to local
        files.save_summoner(result)
        
        return result

def get_recent_games(sumid, force_reload=False):
    """
    Gets recent games by summoner id.
    """
    # Make sure summoner id
    if sumid == None:
        return None
        
    # Request locally
    file_result = files.get_recent_games(sumid)
    if file_result != None and not force_reload:
        if debug:
            print(dbg_str + 'FOUND GAMES IN LOCAL CACHE')
            
        return file_result
    
    result = _get(1.3, 'game/by-summoner/{}/recent'.format(sumid))
    
    # Notify user on HTTP error codes
    if type(result) == int:
        if result == 404:
            print('That name couldn\'t be found on this server.')
        elif result == 400:
            print('An internal error occured while contacting '
                   'the server!')
        elif result == 500:
            print('Servers are experiencing difficulties, try again.')
        else:
            print('An unknown error occured! ({})'.format(result))
    else:
        # Convert from json format to dict
        result = result.json()
        
        # Save to local
        files.save_recent_games(result)
        
        return result
    
    return result.json()
