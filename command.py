""" Command line base """
# pylint: disable-msg=C0103
from commands.greet_command import GreetCommand
from commands.determine_score import DetermineScoreCommand
from cleo import Application

application = Application()

### Test Commands
application.add(GreetCommand())

application.add(DetermineScoreCommand())

if __name__ == '__main__':
    application.run()
