'''
Common logging utilities.
'''

import gzip
import logging
import os
import pathlib
import shutil
import time


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
                logger.info('Compressed: {gz}')
                logger.debug('Deleting: {log}')
                os.remove(log)
                logger.debug('Deleted: {log}')

    logger.debug('maintenance() - Finish')


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info('Cynical Common Logging - Start')

    try:
        maintenace()
    except Exception as e:
        logger.exception(e)

    logger.info('Cynical Common Logging - Finish')
