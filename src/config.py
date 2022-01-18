import yaml

config = {}

with open("conf.yaml", "r") as stream:
    try:
        config.update(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
        print('Configuration file not found!')