import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """This class contains environmental variables needed for app to
        run 

    Args:
        object (application): this takes the flask app as arg
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_TYPE = 'filesystem'