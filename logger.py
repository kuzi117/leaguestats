from util import Singleton

import datetime
import os

_wrn_str = 'WARNING: '

class Logger(metaclass=Singleton):
    """
    Logging class.

    log levels:
        0 = No logging
        1 = To log file
        2 = To terminal

    Log file defaults to cwd and "{datetime}.log"
    """

    def __init__(self):
        """
        Initializes basic things log level, filepath, and filename.

        If these need to be changed then use the accessors provided.
        """
        self._log_level = 0
        self._file_path = os.getcwd()
        self._file_name = file_name + '.log'

        self._max_log_level = 2

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, path):
        if not os.path.exists(path):
            self.warn('Attempted to set log file path to invalid path. ({})'.format(path))
            return

        self._file_path = path

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, name):
        self._file_name = name + '.log'

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level):
        if level > self._max_log_level:
            self.warn('Attempted to set log level to invalid level. ({})'.format(level))
            self._log_level = self._max_log_level
        elif level < 0:
            self.warn('Attempted to set log level to invalid level. ({})'.format(level))
            self._log_level = 0
        else:
            self._log_level = level

    def log(self, message):
        """
        Log a message to a destination determined by the log level.
        """
        # Strings
        dt_str = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
        log_str = 'LOG: '
        nl = '\n'

        # No logging
        if self._log_level == 0:
            pass

        # To file
        elif self._log_level == 1:
            with open(self._file_path + os.path.sep + self._file_name, 'a') as log_file:
                log_file.write(dt_str + log_str + message + nl)

        # To console
        elif self._log_level == 2:
            print(log_str + message)

        # Bad log level, send to warn
        else:
            self.error('Bad log level in log! ({})'.format(self._log_level))

    def warn(self, message):
        """
        Log a warning message to a destination determined by the log level.
        """
        # Strings
        dt_str = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
        warn_str = 'WARNING: '
        nl = '\n'

        # No logging
        if self._log_level == 0:
            pass

        # To file
        elif self._log_level == 1:
            with open(self._file_path + os.path.sep + self._file_name, 'a') as log_file:
                log_file.write(dt_str + warn_str + message + nl)

                        # To console
        elif self._log_level == 2:
            print(warn_str + message)

        # Bad log level
        else:
            self.error('Bad log level in warn! ({})'.format(self._log_level))

    def error(self, message):
        """
        Logs an error message to a destination determined by the log level.

        Handles bad log levels better than other logging functions
        """
        # Strings
        dt_str = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
        err_str = 'ERROR: '
        nl = '\n'

        # No logging
        if self._log_level == 0:
            pass

        # To file
        elif self._log_level == 1:
            with open(self._file_path + os.path.sep + self._file_name, 'a') as log_file:
                log_file.write(dt_str + err_str + message + nl)

                        # To console
        elif self._log_level == 2:
            print(err_str + message)

        # Bad log level
        else:
            # Print for now, will become more sophisticated when app leaves CL
            print(err_str + 'Bad log level, error message requested ({})!'.format(message))






