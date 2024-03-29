import json

from model import LunarCalendarData


def load_json(file_path: str) -> list[dict[str, any]]:
    with open(file_path) as f:
        json_data = json.load(f)

    return json_data


def convert_data(json_data: list[dict[str, any]]) -> list[LunarCalendarData]:
    def to_model(metadata: dict[str, any]) -> LunarCalendarData:
        date: str = metadata['date']
        summery: str = metadata['summery']
        years: int = metadata['years']
        month = int(date[0:2])
        day = int(date[2:])

        return LunarCalendarData(month, day, summery, years)

    return [to_model(metadata) for metadata in json_data]


def load_data(file_path: str) -> list[LunarCalendarData]:
    return convert_data(load_json(file_path))
