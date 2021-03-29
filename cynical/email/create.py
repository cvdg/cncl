import os
import sqlite3
import sys

import cynical.common.iso6346


def create_email(db):
    PREFIX = 'cvdg'
    DOMAIN = 'griend.eu'
    FORWARD = 'cees@griend.eu'

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('SELECT sequence FROM sequence WHERE name = ?', (PREFIX,))
    serial = cur.fetchone()[0]
    cur.execute(
        "UPDATE sequence SET sequence = sequence + 1, date_used = (datetime('now', 'localtime')) WHERE name = ?",
        (PREFIX,))

    tmp = f'{PREFIX}{serial:06}'
    alias = cynical.common.iso6346.create(tmp)
    receiver = f'{alias}@{DOMAIN}'

    cur.execute('INSERT INTO alias (alias, forward) VALUES(?, ?)', (alias, FORWARD,))
    cur.execute('INSERT INTO receiver (receiver, alias) VALUES(?, ?)', (receiver, alias,))

    print(f'Created: {receiver}')

    con.commit()
    con.close()

    return receiver


if __name__ == '__main__':
    db = os.environ.get('CYNICAL_DB')

    if not db:
        dbdir = os.path.join(home, 'var', 'opt', 'cynical')
        db = os.path.join(dbdir, 'cynical-email.db')

        if not os.path.isdir(dbdir):
            os.makedirs(dbdir)

    if not os.path.isfile(db):
        print('Error: {db} does not exist')
        sys.exit(1)

    receiver = create_email(db)
