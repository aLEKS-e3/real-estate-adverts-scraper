import csv
import json


def write_to_json(filename: str, data: list[dict]) -> None:
    with open(filename, "w") as file:
        json.dump(data, file)


def read_json(filename: str) -> list:
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def write_to_csv(filename: str, data: list[dict]) -> None:
    columns = data[0].keys()

    with open(filename, "w") as file:
        dict_writer = csv.DictWriter(file, columns)
        dict_writer.writeheader()
        dict_writer.writerows(data)
