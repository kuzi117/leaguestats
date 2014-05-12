import logger
import request_manager
import stat_manager
import scheduler

import sys

def main():

    # Logger
    log = logger.Logger()
    log.log_level = 2 # Only set the log level, all other defaults are fine
    
    # Managers
    stats = stat_manager.StatManager()
    reqs = request_manager.RequestManager()

    # Scheduler
    sched = scheduler.Scheduler()
    
    try:
        while True:
            test(reqs, sched)
    except (KeyboardInterrupt, SystemExit) as e:
        log.log('\nClosing up shop...')
        reqs.exit()
        stats.exit()
        sched.exit()
        log.log('Bye bye!')
    except EOFError as e:
        log.warn('\nClosing without saving... :(')
    
def test(reqs, scheduler):
    """
    Function for testing functionality.
    """
    cmd = input('CMD: ').lower()

    if cmd not in ['thread', 'update', 'exit']:
        return

    if cmd == 'exit':
        sys.exit(0)

    if cmd == 'thread':
        names = input('Names: ').lower().replace(' ', '').split(',')

        summoners = reqs.summoners_by_name(names, 'na')

        # Try again
        if summoners == None:
            return

        missing = []
        for name in names:
            if name not in summoners:
                missing.append(name)

        logger.Logger().log('Requesting update thread. Missing: {}'.format(missing))
        scheduler.recent_games_updater({'na':summoners}, 30)

    if cmd == 'update':
        names = input('Name: ').lower().replace(' ', '').split(',')

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
