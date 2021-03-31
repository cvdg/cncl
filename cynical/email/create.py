import logging
import random
import sqlite3

from cynical import config
import cynical.common.iso6346


def execute(db):
    logger = logging.getLogger(__name__)
    logger.debug('execute() - Start')
    PREFIX = 'cvdg'
    DOMAIN = 'griend.eu'
    FORWARD = 'cees@griend.eu'
    rnd = random.randrange(100)
    
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('SELECT sequence FROM sequence WHERE name = ?', (PREFIX,))
    serial = cur.fetchone()[0]

    if serial < 0 or serial > 9999:
        raise Exception(f'serial not in range: {serial}')

    cur.execute(
        "UPDATE sequence SET sequence = sequence + 1, date_used = (datetime('now', 'localtime')) WHERE name = ?",
        (PREFIX,))

    tmp = f'{PREFIX}{serial:04}{rnd:02}'
    alias = cynical.common.iso6346.create(tmp)
    receiver = f'{alias}@{DOMAIN}'

    cur.execute('INSERT INTO alias (alias, forward) VALUES(?, ?)', (alias, FORWARD,))
    cur.execute('INSERT INTO receiver (receiver, alias) VALUES(?, ?)', (receiver, alias,))

    logger.info(f'Created: {receiver}')

    con.commit()
    con.close()

    logger.debug('execute() - Finish')

    return receiver


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info('Cynical Email Create - Start')

    try:
        db = config['db']
        receiver = execute(db)

        print(f'Created: {receiver}')
    except Exception as e:
        logger.exception(e)


    logger.info('Cynical Email Create - Finish')
