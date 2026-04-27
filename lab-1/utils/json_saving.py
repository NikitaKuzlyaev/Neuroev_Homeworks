import json
from typing import (
    Any,
    List,
)


def save_list_to_json(data: List[Any], file_path: str, *, indent: int = 2) -> None:
    """
    Сохраняет список (включая вложенные структуры) в JSON-файл.

    :param data: список для сохранения
    :param file_path: путь к файлу
    :param indent: отступы для форматирования JSON (None = без форматирования)
    """
    if not isinstance(data, list):
        raise TypeError("Ожидается список (list)")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,  # сохраняем Unicode как есть
                indent=indent
            )
    except (TypeError, ValueError) as e:
        # возникает, если объект не сериализуем
        raise ValueError(f"Ошибка сериализации: {e}") from e
    except OSError as e:
        raise OSError(f"Ошибка записи файла: {e}") from e


def load_list_from_json(file_path: str) -> List[Any]:
    """
    Загружает список из JSON-файла.

    :param file_path: путь к файлу
    :return: восстановленный список
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка декодирования JSON: {e}") from e
    except OSError as e:
        raise OSError(f"Ошибка чтения файла: {e}") from e

    if not isinstance(data, list):
        raise TypeError("JSON не содержит список")

    return data
