import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATAVASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tarot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False