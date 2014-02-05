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
        raise
    except EOFError as e:
        print('\nClosing without saving... :(')
    
def test(reqs):
    """
    Function for testing functionality.
    """
    name = input('Name: ')
    if name == 'exit':
        sys.exit(0)
    
    summoner = reqs.summoner_by_name(name, 'na')
    print('\nRESULTS: {}'.format(summoner))
    
    print('\n\n')
    
if __name__ == '__main__':
    debug = True
    main(debug)
