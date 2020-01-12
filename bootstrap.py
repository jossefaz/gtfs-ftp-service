from Configuration.config import Config

if __name__ == '__main__' :
    print("test")
    config = Config()
    print(config.get_property("WS"))
