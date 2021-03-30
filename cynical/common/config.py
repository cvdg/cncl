import logging
import os
import pathlib

import yaml


def __config():
    home_dir = pathlib.Path.home()
    etc_dir = os.path.join(home_dir, 'etc')
    yml = os.path.join(etc_dir, 'cynical.yml')

    if os.path.isfile(yml):
        with open(yml, 'r') as stream:
            data = yaml.safe_load(stream)
    else:
        data = {}

    # default: loglevel
    if not 'loglevel' in data:
        data['loglevel'] = logging.INFO

    # default: ~/Maildir
    if not 'maildir' in data:
        data['maildir'] = os.path.join(home_dir, 'Maildir')

    # default: /var/opt/cynical/cynical-email.db
    if not 'db' in data:
        data['db'] = os.path.join('/var', 'opt', 'cynical', 'cynical-email.db')

    return data


config = __config()


if __name__ == '__main__':
    import pprint

    pprint.pprint(config)