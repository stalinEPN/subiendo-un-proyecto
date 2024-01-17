class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
    
class DevelompmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'mysql-stalinserver.alwaysdata.net'
    MYSQL_USER = '286297'
    MYSQL_PASSWORD = 'stalin21r21'
    MYSQL_DB = 'stalinserver_inalambricos'

config={
    'development':DevelompmentConfig
}