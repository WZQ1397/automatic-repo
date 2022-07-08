import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SERVER_URL = '127.0.0.1:9000'
    AK = os.environ.get('MINIO_ACCESS_KEY') or 'minioadmin'
    SK = os.environ.get('MINIO_SECRET_KEY') or 'minioadmin'
    MINIO_BUCKET = os.environ.get('MINIO_BUCKET') or 'zach'
    SSL_ENABLE = False
    SERVER_LOC = os.environ.get('MINIO_REGION') or "us-east-1"
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
