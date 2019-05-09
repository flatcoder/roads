from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import render_template
from app import create_app
from app.importer import ImportCommand
from app.backup import BackupCommand
from app.models import db
import os

app          = create_app(os.getenv('FLASK_ENV'), db)
migrate      = Migrate(app, db)
manager      = Manager(app)

manager.add_command('database', MigrateCommand)
manager.add_command('import_csv', ImportCommand)
manager.add_command('backup_json', BackupCommand)

@app.route('/')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    manager.run()
