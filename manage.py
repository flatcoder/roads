from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.importer import ImportCommand
from app.models import db

app     = create_app("development", db)
migrate = Migrate(app, db)
manager = Manager(app)

# Support for database migrations and importing CSV data
manager.add_command('database', MigrateCommand)
manager.add_command('import_csv', ImportCommand)

# JS Demo (Client)
@app.route('/')
def demo():
    return 'Client demo in JS'

if __name__ == '__main__':
    manager.run()
