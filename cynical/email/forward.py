import datetime
import email
import logging
import mailbox
import smtplib
import sqlite3

from cynical import config
import cynical.common.logger


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
    backup_name = datetime.datetime.now().strftime('backup%Ym%M')
    backup = folder.add_folder(backup_name)
    delete = []

    for key, msg in folder.iteritems():
        tx = email.utils.parseaddr(msg['From'])[1]
        rx = email.utils.parseaddr(msg['To'])[1]
        subj = msg['Subject']
        id = msg['Message-ID']
        date = email.utils.parsedate_to_datetime(msg['Date'])

        if not is_known(db, id):
            record(db, id, date, tx, rx, subj)

            # Workaround for TransIP
            # msg.replace_header('To', 'c.vande.griend@gmail.com')
            # msg.replace_header('From', 'cees+cynical@griend.eu')

            logger.debug(f'Sending: {id}')
            with smtplib.SMTP('localhost') as smtp:
                smtp.send_message(msg, from_addr='cees+cynical@griend.eu', to_addrs='c.vande.griend@gmail.com')
            logger.info(f'Forward: {id}')
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
    logger = logging.getLogger(__name__)
    logger.info('Cynical Email Forward - Start')

    try:
        mail_dir = config['maildir']
        db = config['db']

        execute(mail_dir, db)

        cynical.common.logger.maintenance()
    except Exception as e:
        logger.exception(e)

    logger.info('Cynical Email Forward - Finish')
