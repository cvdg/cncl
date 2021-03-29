import email
import logging
import mailbox
import os
import pathlib
import smtplib
import sqlite3

from cynical.common.logging import maintenance

def is_known(db, message_id):
    known = True
    con = sqlite3.connect(db)
    cur = con.cursor()

    # Check if Message-ID exists
    cur.execute('SELECT COUNT(message_id) FROM message WHERE message_id = ?', (message_id,))
    if cur.fetchone()[0] == 0:
        known = False

    con.commit()
    con.close()

    return known


def record(db, message_id, message_date, sender, receiver, subject):
    logger = logging.getLogger(__name__)
    logger.debug('record() - Start')

    con = sqlite3.connect(db)
    cur = con.cursor()

    # Check if Sender exists
    cur.execute('SELECT COUNT(sender) FROM sender WHERE sender = ?', (sender,))
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO sender (sender) VALUES(?)', (sender,))

    # Check if Receiver exists
    cur.execute('SELECT COUNT(receiver) FROM receiver WHERE receiver = ?', (receiver,))
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO receiver (receiver) VALUES(?)', (receiver,))

    # Insert message ans Update sender and receiver
    cur.execute('INSERT INTO message (message_id, message_date, sender, receiver, subject) VALUES(?, ?, ?, ?, ?)',
                (message_id, message_date, sender, receiver, subject,))
    cur.execute("UPDATE sender SET date_used = (datetime('now', 'localtime')), used = used + 1 WHERE sender = ?",
                (sender,))
    cur.execute("UPDATE receiver SET date_used = (datetime('now', 'localtime')), used = used + 1 WHERE receiver = ?",
                (receiver,))

    con.commit()
    con.close()
    logger.debug('record() - Finish')


def execute(maildir, db):
    logger = logging.getLogger(__name__)
    logger.debug('execute() - Start')
    logger.debug(f'Maildir: {maildir}')
    logger.debug(f'DB: {db}')

    folder = mailbox.Maildir(maildir)
    backup = folder.add_folder('backup')
    delete = []

    with smtplib.SMTP('localhost') as smtp:
        for key, msg in folder.iteritems():
            tx = email.utils.parseaddr(msg['From'])[1]
            rx = email.utils.parseaddr(msg['To'])[1]
            subj = msg['Subject']
            id = msg['Message-ID']
            date = email.utils.parsedate_to_datetime(msg['Date'])

            if not is_known(db, id):
                record(db, id, date, tx, rx, subj)

                # Workaround for TransIP
                msg.replace_header('To', 'c.vande.griend@gmail.com')
                msg.replace_header('From', 'cees+cynical@griend.eu')

                logger.debug(f'Sending: {id}')
                smtp.send_message(msg, from_addr='cees+cynical@griend.eu', to_addrs='c.vande.griend@gmail.com')
                logger.info(f'Send: {id}')
            else:
                logger.warning(f'Duplicate message: {id}')

            logger.debug(f'Backing up: {id}')
            backup.add(msg)
            logger.info(f'Backed up: {id}')

            delete.append(key)

        backup.flush()
        backup.close()

    for key in delete:
        logger.debug(f'Deleting: {key}')
        folder.remove(key)
        logger.info(f'Deleted: {key}')

    folder.flush()
    folder.close()

    logger.debug('execute() - Finish')


if __name__ == '__main__':
    '''
    CYNICAL_MAILDIR: ~/Maildir/
    CYNICAL_DB:      /var/opt/cynical/cynical-email.db
                     /var/opt/cynical/cynical-email.db
    '''
    logger = logging.getLogger(__name__)
    logger.info('Cynical Email Forward - Start')

    try:
        # ToDo: config in a module
        mail_dir = os.environ.get('CYNICAL_MAILDIR')
        db = os.environ.get('CYNICAL_DB')

        if not mail_dir:
            home = pathlib.Path.home()
            mail_dir = os.path.join(home, 'Maildir')

        if not db:
            db_dir = os.path.join('/var', 'opt', 'cynical')
            db = os.path.join(db_dir, 'cynical-email.db')

        if not os.path.isdir(mail_dir):
            raise Exception('Error: {mail_dir} does not exist')

        if not os.path.isfile(db):
            raise Exception(f'Error: {db} does not exist')

        execute(mail_dir, db)
        maintenance()
    except Exception as e:
        logger.exception(e)

    logger.info('Cynical Email Forward - Finish')
