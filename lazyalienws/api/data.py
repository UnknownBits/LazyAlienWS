import json

class Data:

    def __init__(self, filename:str, default_data:dict|list={}, filepath="data/") -> None:
        self.filename = filename
        self.filepath = filepath
        self.file = filepath+filename
        self.default_data = default_data

    def write(self, data: dict) -> None:
        with open(self.file, "w+", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
            file.close()

    def read(self) -> dict|list:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            file.close()
        return data
    
    def load(self) -> dict|list:
        try:
            data = self.read()
        except:
            self.write(self.default_data)
            data = self.default_data
        return data

class Config(Data):
    
    def __init__(self, filename: str, default_data: dict | list = {}, filepath="conf/") -> None:
        super().__init__(filename, default_data, filepath)