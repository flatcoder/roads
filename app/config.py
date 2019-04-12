import os

class Development(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgres:///roads"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = {
    'development': Development,
    'production': Production,
}

# export FLASK_ENV=development
# export DATABASE_URL= postgres://name:password@houst:port/blog_api_db
# export JWT_SECRET_KEY = hhgaghhgsdhdhdd
