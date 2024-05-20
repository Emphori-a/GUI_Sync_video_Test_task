"""Модуль со вспомогательными функциями для работы с файлами.

read_annotations: функция для считывания аннотаций.
check_files_exist: функция для проверки существования необходимых файлов.
validate_annotations: функция проверки аннотаций на соответствие видеофайлам.
"""

import os
from typing import Dict, List

from core import ANNOTATION_EXTENSION


def read_annotations(folder_path: str) -> Dict[str, List[float]]:
    """
    Чтение аннотаций из файлов в папке.

    Параметры:
        folder_path (str): Путь к папке с аннотациями.

    Возвращает:
        dict: Словарь, где ключами являются названия видеофайлов,
              а значениями - списки временных меток из аннотаций.

    Формат аннотаций:
        - Формат файла: по умолчанию текстовый (.txt).
            Возможно изменить в core.py.
        - Каждая строка файла содержит одну временную метку.
        - Каждая строка файла характеризует один кадр видео.

    Исключения:
        - FileNotFoundError: Если файл аннотаций не найден.
        - ValueError: Если аннотации содержат некорректные данные.
    """
    annotations = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(ANNOTATION_EXTENSION):
            video_name = os.path.splitext(filename)[0]
            try:
                with open(os.path.join(folder_path, filename), 'r') as file:
                    lines = file.readlines()
                    timestamps = []
                    for line in lines:
                        try:
                            timestamps.append(float(line.strip()))
                        except ValueError:
                            raise ValueError(
                                "Некорректная временная метка в файле "
                                f"аннотаций {filename}: {line.strip()}")
                    annotations[video_name] = timestamps
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Файл аннотаций {filename} не найден.")
    return annotations


def check_files_exist(video_paths: List[str], annotation_folder: str) -> bool:
    """
    Проверка существования видео-файлов и файлов аннотаций.

    Параметры:
        video_paths (List[str]): Список путей к видеофайлам.
        annotation_folder (str): Путь к папке с файлами аннотаций.

    Возвращает:
        bool: True, если все файлы существуют, и False в противном случае.
    """
    files_exist = all(os.path.isfile(path) for path in video_paths)
    annotation_files_exist = all(
        os.path.isfile(os.path.join(annotation_folder, filename))
        for filename in os.listdir(annotation_folder)
        if filename.endswith(ANNOTATION_EXTENSION)
    )
    return files_exist and annotation_files_exist


def validate_annotations(video_paths: List[str],
                         annotations: Dict[str, List[float]]) -> None:
    """
    Проверка аннотаций на соответствие видеофайлам.

    Параметры:
        video_paths (List[str]): Список путей к видеофайлам.
        annotations (Dict[str, List[float]]): Словарь аннотаций.

    Исключения:
        ValueError: Если аннотации отсутствуют для какого-либо видеофайла
                    или если аннотации пустые.
    """
    for video_path in video_paths:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        if video_name not in annotations:
            raise ValueError(
                f"Аннотации отсутствуют для видеофайла {video_name}.")
        if not annotations[video_name]:
            raise ValueError(
                f"Файл аннотаций для видеофайла {video_name} пуст.")
