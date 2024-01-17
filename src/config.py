class Config:
    SECRET_KEY = ''
    
class DevelompmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = ''
    MYSQL_USER = ''
    MYSQL_PASSWORD = ''
    MYSQL_DB = ''

config={
    'development':DevelompmentConfig
}
