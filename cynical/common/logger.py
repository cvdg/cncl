'''
Common logging utilities.
'''

import datetime
import gzip
import logging
import os
import pathlib
import shutil
import time

def setup(loglevel):
    """
    Creates a console handler with loglevel ERROR and a
    file handler with the given loglevel.

    """
    log_directory = os.path.join(pathlib.Path.home(), 'var', 'log', 'cynical')
    log_filename = os.path.join(log_directory, datetime.datetime.now().strftime('%Y%m%d.log'))

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Creates console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)

    # Get the ROOT logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # Creates logfile
    fh = logging.FileHandler(log_filename)
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)

    logger.addHandler(fh)


def maintenance():
    logger = logging.getLogger(__name__)
    logger.debug('maintenance() - Start')

    log_directory = os.path.join(pathlib.Path.home(), 'var', 'log', 'cynical')
    now = time.time()
    two_days_ago = now - 2 * 24 * 60 * 60

    for entry in os.listdir(log_directory):
        log = os.path.join(log_directory, entry)
        if os.path.isfile(log) and log.endswith('.log'):
            mtime = os.path.getmtime(log)
            if mtime < two_days_ago:
                # compress
                gz = f'{log}.gz'
                logger.debug(f'Compressing: {log}')
                with open(log, 'rb') as f_in:
                    with gzip.open(gz, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.utime(gz, (mtime, mtime,))
                logger.info(f'Compressed: {gz}')
                logger.debug(f'Deleting: {log}')
                os.remove(log)
                logger.debug(f'Deleted: {log}')

    logger.debug('maintenance() - Finish')


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info('Cynical Common Logging - Start')

    try:
        maintenace()
    except Exception as e:
        logger.exception(e)

    logger.info('Cynical Common Logging - Finish')
