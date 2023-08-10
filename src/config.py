from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY')
    UPLOAD_FOLDER = config('UPLOAD_FOLDER')
    #CAPTCHA_CONFIG = {'SECRET_CAPTCHA_KEY': config('SECRET_CAPTCHA_KEY')}

class DevelopmentConfig(Config):
    DEBUG = config('DEBUG')
    MYSQL_HOST = config('MYSQL_HOST')
    MYSQL_USER = config('MYSQL_USER')
    MYSQL_PASSWORD = config('MYSQL_PASSWORD')
    MYSQL_DB = config('MYSQL_DB')

config = {
    "development" : DevelopmentConfig
}