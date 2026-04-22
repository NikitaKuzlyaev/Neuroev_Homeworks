import yaml


class YAMLReader:

    @staticmethod
    def yaml_2_map(path: str, op: str = "r", encoding: str = "utf-8") -> dict:
        with open(f"{path}", op, encoding=encoding) as f:
            data = yaml.safe_load(f)
            return data
