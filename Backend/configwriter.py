from configparser import ConfigParser

config = ConfigParser()

config["mongodb"] = {
    "host": "localhost",
    "port": "27017"

}

with open("config.ini", "w") as f:
    config.write(f)