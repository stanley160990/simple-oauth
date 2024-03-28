import yaml
import os

class Config(object):
    def __init__(self, args1):
        self.args1 = args1
    
    # def get(self):
    #     kind = self.args1

    #     with open('etc/config.yml') as yamlfile:
    #         cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)

    #     if kind == 'postgresql0':
    #         host = cfg["postgres0"]["host"]
    #         port = cfg["postgres0"]["port"]
    #         database = cfg["postgres0"]["database"]
    #         username = cfg["postgres0"]["username"]
    #         password = cfg["postgres0"]["password"]

    #         return host, port, database, username, password
    #     elif kind == 'redis':
    #         host = cfg["redis"]["host"]
    #         port = cfg["redis"]["port"]
    #         database = cfg["redis"]["database"]
    #         password = cfg["redis"]["password"]

    #         return host, port, database, password
    
    def get(self):
        kind = self.args1

        if kind == 'postgresql0':
            host = os.environ['POSTGRES_HOST']
            port = os.environ['POSTGRES_PORT']
            database = os.environ['POSTGRES_DB']
            username = os.environ['POSTGRES_USER']
            password = os.environ['POSTGRES_PASSWORD']

            return host, port, database, username, password