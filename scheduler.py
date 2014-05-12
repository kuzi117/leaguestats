from util import Singleton
import logger
import request_manager

import threading


class Scheduler(metaclass=Singleton):
    def __init__(self):
        # Logger
        self.log = logger.Logger()

        # Dict of active threads
        self.threads = {}

    def recent_games_updater(self, summoners, delay):
        """
        Start the updater.
        """
        if 'games_updater' in self.threads:
            raise NotImplementedError('Updating the list of summoners to update isn\'t implemented yet.')
        else:
            self.threads['games_update'] = updater = UpdateGamesThread(summoners, delay)
            updater.start()

    def exit(self):
        """
        Prepares for exit.
        """
        self.log.log('Scheduler closing active threads.')
        for thread in self.threads:
            self.threads[thread].exit()


class UpdateGamesThread(threading.Thread):
    """
    Mostly a copy of threading.Timer, with minor changes to allow the action to repeat.
    """
    def __init__(self, summoners, interval):
        threading.Thread.__init__(self, daemon=True)

        self.name = 'GamesUpdaterThread'

        self.log = logger.Logger()

        # Action things
        self.summoners = summoners

        # Timer things
        self.interval = interval
        self.finished = threading.Event()
        self.log.log('GamesUpdater thread created. (Interval: {}s, Summoners: {})'.format(self.interval,
                                                                                          self.summoners))

        # Managers
        self.logger = None
        self.reqs = None

    def cancel(self):
        """
        Stop the actions.
        """
        # Close managers in this thread
        self.reqs.exit()

        self.log.log('GamesUpdater canceling base thread.')
        self.finished.set()

    def exit(self):
        """
        Calls cancel. Implemented to allow common interface with other custom threads.
        """
        self.log.log('GamesUpdater exiting.')
        self.cancel()

    def run(self):
        """
        Run repeatedly.
        """
        # Initialize things in this thread
        self.reqs = request_manager.RequestManager()
        self.log = logger.Logger()

        first = True

        while not self.finished.is_set():
            # Wait, first time only for 5 seconds
            if first:
                first = False
                self.finished.wait(5)
            else:
                self.finished.wait(self.interval)

            # If still good
            if not self.finished.is_set():
                # Log
                self.log.log('GamesUpdater running update..')
                self.log.log('Summoners to update: {}'.format(self.summoners))

                # for each region, for each summoner
                for region in self.summoners:
                    for name in self.summoners[region]:
                        summoner = self.summoners[region][name]
                        self.reqs.recent_games(summoner['id'], region)

                self.log.log('GamesUpdater done updating.')

        self.log.log('GamesUpdater finishing run.')

