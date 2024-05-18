"""Модуль с описанием класса для окна интерфейса."""
import os
from typing import Dict, List

from PyQt5.QtWidgets import (QGridLayout, QLabel, QMainWindow,
                             QPushButton, QWidget)

from core import FRAME_RATE
from video_player import VideoPlayer


class MainWindow(QMainWindow):
    """Главное окно приложения видеоплеера.

    Аргументы:
        video_paths (List[str]): Список путей к видеофайлам.
        annotations (Dict[str, List[float]]):
                    Словарь аннотаций для видеофайлов.

    Атрибуты:
        video_paths (List[str]): Список путей к видеофайлам.
        annotations (Dict[str, List[float]]):
                    Словарь аннотаций для видеофайлов.
        central_widget (QWidget): Центральный виджет главного окна.
        layout (QGridLayout): Макет главного окна.
        video_players (List[VideoPlayer]): Список видеоплееров для видеофайлов.
    """

    def __init__(self, video_paths: List[str],
                 annotations: Dict[str, List[float]]):
        super().__init__()

        self.setWindowTitle("Sync_video_GUI")
        self.video_paths = video_paths
        self.annotations = annotations

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.play_button = QPushButton("Начать воспроизведение")
        self.layout.addWidget(self.play_button, 0, 0)
        self.play_button.clicked.connect(self.start_all_videos)

        self.stop_button = QPushButton("Остановить воспроизведение")
        self.layout.addWidget(self.stop_button, 0, 1)
        self.stop_button.clicked.connect(self.stop_all_videos)

        self.video_players = []
        self.set_videoplayers()

    def set_videoplayers(self) -> None:
        """Создает видеоплееры для каждого видеофайла.
        Добавляет их на главное окно."""
        min_timestamp = int(min(annot[0]
                                for annot in self.annotations.values()))
        initial_row_offset = 1
        for idx, video_path in enumerate(self.video_paths):
            label = QLabel()
            title_label = QLabel(os.path.basename(video_path))
            row, col = divmod(idx, 2)
            row = (row * 2) + initial_row_offset
            self.layout.addWidget(title_label, row, col)
            self.layout.addWidget(label, row+1, col)
            video_player = VideoPlayer(video_path, label, self.annotations.get(
                os.path.splitext(os.path.basename(video_path))[0], []),
                min_timestamp, frame_rate=FRAME_RATE)
            self.video_players.append(video_player)

    def closeEvent(self, event) -> None:
        """Обработчик события закрытия окна.

        Аргументы:
            event: Событие закрытия окна.
        """
        for player in self.video_players:
            player.close()
        super().closeEvent(event)

    def start_all_videos(self):
        """Метод для запуска воспроизведения всех видео."""
        for player in self.video_players:
            player.start_playing()

    def stop_all_videos(self):
        """Метод для остановки воспроизведения всех видео."""
        for player in self.video_players:
            player.stop_playing()
