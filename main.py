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
    names = input('Name: ').lower().replace(' ', '').split(',')
    if 'exit' in names:
        sys.exit(0)
    
    summoners = reqs.summoners_by_name(names, 'na')

    # Try again
    if summoners == None:
        return

    missing = []
    for name in names:
        if name in summoners:
            reqs.recent_games(summoners[name]['id'], 'na')
        else:
            missing.append(name)

    print('Games loaded and saved. Missing: {}'.format(names))
    
    print('\n\n')
    
if __name__ == '__main__':
    debug = True
    main(debug)
