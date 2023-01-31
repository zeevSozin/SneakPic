from configparser import ConfigParser

config = ConfigParser()

config["endpoint"] = {
    "host": "localhost",
    "port": "8080",
    "baseRoute": "v1"

}

with open("config.ini", "w") as f:
    config.write(f)