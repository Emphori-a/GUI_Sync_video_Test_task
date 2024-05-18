"""Модуль с описанием основной функции для запуска GUI."""

import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from core import FILE_EXTENSION, VIDEO_FOLDER
from gui import MainWindow
from utils import check_files_exist, read_annotations


def main() -> None:
    """Основная функция для запуска приложения видеоплеера."""

    video_paths = [os.path.join(VIDEO_FOLDER, f"{i}.{FILE_EXTENSION}")
                   for i in range(1, 5)]

    if not check_files_exist(video_paths, VIDEO_FOLDER):
        print("Один или несколько файлов отсутствуют.")
        return

    try:
        annotations = read_annotations(VIDEO_FOLDER)
    except FileNotFoundError as e:
        QMessageBox.critical(None, "Ошибка",
                             f"Ошибка при чтении аннотаций: {e}. "
                             "Проверьте, что файлы аннотаций в папке data "
                             "соответствуют видеофайлам.")
        return
    except ValueError as e:
        QMessageBox.critical(
            None, "Ошибка", f"Ошибка при чтении аннотаций: {e}. Проверьте "
            "формат файлов аннотаций и их соответствие видеофайлам.")

    app = QApplication(sys.argv)
    try:
        window = MainWindow(video_paths, annotations)
    except Exception as e:
        QMessageBox.critical(None, "Ошибка",
                             f"Ошибка при запуске приложения: {e}")
        return

    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
