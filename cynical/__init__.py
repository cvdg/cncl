import datetime
import logging
import os
import pathlib

__author__ = 'Cees van de Griend <cees@griend.eu>'


def setup_logging(loglevel=logging.DEBUG):
    """
    Creates a console handler with loglevel INFO and a
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


setup_logging()
