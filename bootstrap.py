from Configuration.config import Config

if __name__ == '__main__' :

    config = Config()
    print(config.get_property("WS"))
