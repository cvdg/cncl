import cmd
import logging

from cynical import config

import cynical.common.logger
import cynical.email.create

class EmailShell(cmd.Cmd):
    intro = 'Welcome to the email shell. Type help or ? to list commands.'
    prompt = 'email> '

    def do_create(self, arg):
        'Create a email alias: CREATE [N]'

        db = config['db']

        if len(arg) == 0:
            n = 1
        else:
            n = int(arg.split()[0])

        for i in range(n):
            receiver = cynical.email.create.execute(db)
            print(f'Created: {receiver}')

    def do_echo(selfself, arg):
        'Echo the arguments: ECHO [...]'
        print('Echo: ', arg)

    def do_maintenance(self, arg):
        'Maintenance compresses logfiles: MAINTENANCE'
        cynical.common.logger.maintenance()

    def do_quit(self, arg):
        'Quit stops the shell : QUIT'
        return True

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info('Cynical Email - Start')

    try:
        EmailShell().cmdloop()
    except Exception as e:
        logger.exception(e)

    logger.info('Cynical Email - Finish')
