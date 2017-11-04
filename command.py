""" Command line base """
# pylint: disable-msg=C0103
from commands.greet_command import GreetCommand
from cleo import Application

application = Application()

### Test Commands
application.add(GreetCommand())

if __name__ == '__main__':
    application.run()
