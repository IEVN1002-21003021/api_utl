class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST='localhost'
    MSQL_USER='root'
    MYSQL_PASSWORD=''
    MYSQL_DB='api_utl'

config = {
        'development': DevelopmentConfig
    }