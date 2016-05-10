import os


MONGODB_HOST = os.getenv('MONGODB_HOST', 'mongo_instance_001')
MONGODB_PORT = os.getenv('MONGODB_PORT', '27017')
MONGODB_USER = os.getenv('MONGODB_USER', '')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', '')
MONGODB_DB = os.getenv('MONGODB_DATABASE', 'pymicroservice')
DEBUG = os.getenv('DEBUG_MODE', 'False')

