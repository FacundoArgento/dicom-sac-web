from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY')
    TEMP_FOLDER = config('TEMP_FOLDER')
    AK = config('AK')
    SK = config('SK')
    HUAWEI_SERVER = config('HUAWEI_SERVER')
    BUCKET_NAME = config('BUCKET_NAME')
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