from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.importer import ImportCommand
from app.models import db
import os

app     = create_app(os.getenv('FLASK_ENV'), db)
migrate = Migrate(app, db)
manager = Manager(app)

# Support for database migrations and importing CSV data
manager.add_command('database', MigrateCommand)
manager.add_command('import_csv', ImportCommand)

@app.route('/')
def home():
    return 'CP API ENDPOINT'

if __name__ == '__main__':
    manager.run()
