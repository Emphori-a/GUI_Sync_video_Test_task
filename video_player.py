"""Модуль с описанием класса видео-плеера и его методов."""

import logging
import os
from typing import List

import cv2
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer


class VideoPlayer:
    """
    Класс для представления видеоплеера.

    Атрибуты:
        video_path (str): Путь к видеофайлу.
        label (QLabel): Виджет QLabel для отображения кадров видео.
        annotations (List[float]): Список временных меток к видеофайлу.
                        Каждая временная метка характеризует один кадр видео.
        min_timestamp (int): Минимальное значение временной метки.
        frame_rate (int): Частота кадров видео.
        timer (QTimer): Таймер для воспроизведения видео.
        cap: Объект VideoCapture для чтения кадров из видеофайла.
        num_frame (int): номер кадра, первоначально равен 0.
        current_timestamp (float): текущая временная метка.
        frame_counte (int): счетчик кадров.
        previous_frame: сохраненный предыдущий кадр.
        use_old_frame (bool): флаг, указывающий на использование старого кадра.
    """

    def __init__(self, video_path: str, label: QLabel,
                 annotations: List[float], min_timestamp: int,
                 frame_rate: int):
        """
        Инициализация видеоплеера.

        Параметры:
            video_path (str): Путь к видеофайлу.
            label (QLabel): Виджет QLabel для отображения кадров видео.
            annotations (List[float]): Список временных меток к видеофайлу.
            min_timestamp (int): Минимальное значение временной метки.
            frame_rate (int): Частота кадров видео.
        """
        self.video_path = video_path
        self.label = label
        self.annotations = annotations
        self.min_timestamp = min_timestamp
        self.frame_rate = frame_rate
        self.timer = QTimer()
        self.cap = cv2.VideoCapture(self.video_path)
        self.num_frame = 0
        self.current_timestamp = self.annotations[self.num_frame]
        self.frame_counter = 0

        self.previous_frame = None
        self.use_old_frame = False

        logging.basicConfig(filename='video_player.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        try:
            self.check_videofile()
            self.check_annotations()
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", str(e))
            raise

    def play(self) -> None:
        """Воспроизведение видео на виджете QLabel."""
        ret, frame = self.cap.read()
        if ret:
            self.previous_frame = frame.copy()
            if self.use_old_frame:
                frame = self.add_old_frame_label(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(
                frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_qt_format.scaled(
                self.label.width(), self.label.height(), Qt.KeepAspectRatio
            )
            self.label.setPixmap(QPixmap.fromImage(p))
            self.frame_counter += 1

            # Логгирование информации о кадре
            video_name = os.path.basename(self.video_path)
            logging.info(f"Video: {video_name}, Frame: {self.num_frame}, "
                         f"Timestamp: {self.current_timestamp}")

            self.get_next_frame()
        else:
            if self.previous_frame is not None:
                frame = self.previous_frame.copy()
                frame = self.add_old_frame_label(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line,
                                              QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(
                    self.label.width(), self.label.height(), Qt.KeepAspectRatio
                )
                self.label.setPixmap(QPixmap.fromImage(p))

            QMessageBox.warning(None, "Предупреждение",
                                (f"Не удалось прочитать кадр {self.num_frame}."
                                 " Пропускаем кадр."))
            self.get_next_frame()

    def add_old_frame_label(self, frame):
        """Добавляет метку на кадр, чтобы указать, что кадр старый."""
        text = "Old_frame"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        font_scale = 1
        color = (0, 0, 255)
        thickness = 2
        frame = cv2.putText(frame, text, org, font, font_scale,
                            color, thickness, cv2.LINE_AA)
        return frame

    def get_next_frame(self) -> None:
        """Определение следующего кадра для воспроизведения."""
        if self.num_frame + 1 < len(self.annotations):
            next_timestamp = self.annotations[self.num_frame + 1]
            if int(self.current_timestamp) - self.min_timestamp < 1:
                self.min_timestamp = int(self.current_timestamp)

            if int(next_timestamp) - self.min_timestamp < 1:
                self.num_frame += 1
                self.current_timestamp = next_timestamp
            else:
                self.use_old_frame = True

            if self.frame_counter == self.frame_rate:
                if int(self.current_timestamp) - self.min_timestamp < 1:
                    self.num_frame += 1
                    self.current_timestamp = self.annotations[
                        self.num_frame]
                    self.min_timestamp = int(self.current_timestamp)
                    self.frame_counter = 0
                    self.use_old_frame = False
                else:
                    self.min_timestamp = int(self.current_timestamp)
                    self.frame_counter = 0
                    self.use_old_frame = True
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.num_frame)
        else:
            self.stop_playing()

    def check_annotations(self) -> None:
        """Проверка наличия аннотаций и их соответствия видео."""
        if (len(self.annotations) == 0 or len(self.annotations) != int(
                self.cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            raise ValueError(
                "Количество аннотаций не соответствует количеству кадров.")

    def check_videofile(self):
        """Проверка корректности открытия видеофайла."""
        if not self.cap.isOpened():
            raise FileNotFoundError(
                f"Невозможно открыть видеофайл: {self.video_path}")

    def start_playing(self) -> None:
        """Начать воспроизведение видео."""
        self.timer.timeout.connect(self.play)
        self.timer.start(int(1000 / self.frame_rate))

    def stop_playing(self):
        """Метод для остановки воспроизведения видео."""
        self.timer.stop()

    def close(self) -> None:
        """Закрыть видеопоток."""
        if self.cap is not None:
            self.cap.release()
