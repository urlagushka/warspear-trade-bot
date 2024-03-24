import json


# Config structs that loads config files

class Inf:
    def __init__(self, inf_path: str):
        with open(inf_path, encoding='utf-8') as file:
            data = json.load(file)
            self.trade = data["trade"]


class Config:
    def __init__(self, cnf_path: str):
        with open(cnf_path, encoding='utf-8') as file:
            data = json.load(file)
            self.timeout = data["timeout"]
            self.configs = data["windows"]
