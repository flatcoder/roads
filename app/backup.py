from flask_script import Command, Option
from app.models import ModelABC

class BackupCommand(Command):
    "Backup the database to a timestamped file."

    option_list = (
        Option('--file', '-f', dest='filename'),
    )

    def run(self,filename):
        if filename == None:
            print("No output file specified. Use -? for help.")
            return False

        print("Backing up database to "+filename+".")
        test=ModelABC.backup_database(filename)
        print(test)
