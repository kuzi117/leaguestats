import request_manager
import stat_manager
from util import dbg_str

import sys

def main(debug = False):
    
    # Managers
    stats = stat_manager.StatManager(debug = debug)
    reqs = request_manager.RequestManager(debug = debug)
    
    try:
        while True:
            test(reqs)
    except (KeyboardInterrupt, SystemExit) as e:
        print('\nClosing up shop...')
        reqs.exit()
        stats.exit()
        print('Bye bye!')
    except EOFError as e:
        print('\nClosing without saving... :(')
    
def test(reqs):
    """
    Function for testing functionality.
    """
    name = input('Name: ').lower().replace(' ', '')
    if name == 'exit':
        sys.exit(0)
    
    summoner = reqs.summoners_by_name([name], 'na')

    # Try again
    if summoner == None:
        return

    recents = reqs.recent_games(summoner[name]['id'], 'na')
    print('Games loaded and saved.')
    
    print('\n\n')
    
if __name__ == '__main__':
    debug = True
    main(debug)
