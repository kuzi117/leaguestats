import logger
import request_manager
import stat_manager

import sys

def main():
    
    # Managers
    stats = stat_manager.StatManager()
    reqs = request_manager.RequestManager()

    # Logger
    log = logger.Logger()
    log.log_level = 1 # Only set the log level, all other defaults are fine
    
    try:
        while True:
            test(reqs)
    except (KeyboardInterrupt, SystemExit) as e:
        log.log('Closing up shop...')
        reqs.exit()
        stats.exit()
        log.log('Bye bye!')
    except EOFError as e:
        log.warn('\nClosing without saving... :(')
    
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

    logger.Logger().log('Games loaded and saved. Missing: {}'.format(missing))
    
if __name__ == '__main__':
    main()
