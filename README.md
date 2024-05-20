# Video Player

## Описание  
Video Player - это приложение для синхронного воспроизведения четырех видео. Для синхронного воспроизведения видео используются файлы-аннотации, содержащие временные метки для каждого кадра видео. 

### Задание  
Видео рассинхронизированы, в них пропущены некоторые кадры. Частота кадров: 5. Если для момента времени у какого-то видео отсутствует кадр, то отображается предыдущий кадр. Если отображается предыдущий кадр, на изображении кадра добавляется метка "Old_frame".

## Использованные технологии

- Язык программирования: Python 3.9
- OpenCV
- PyQt5

## Установка и запуск приложения.

### Установка:

1. Создайте и активируйте виртуальное окружение:

- Если у вас Linux/macOS:
    ```
    python3.9 -m venv venv
    source venv/bin/activate
    ```
 - Если у вас Windows:
    ```
    py -3.9 -m venv venv
    source venv/Scripts/activate
    ```
2. Обновите установщик пакетов pip:
```
python -m pip install --upgrade pip
```
3. Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. В корневой директории проекта создайте папку 'data' и разместите в ней 4 видео-файла и 4 файла-аннотации.

### Запуск приложения  

Приложение запускается командой 
```
python main.py
```

## Использование

После запуска приложения откроется окно интерфейса, где можно запустить воспроизведение видео. Видео будут синхронизированы в соответствии с аннотациями.

## Примечания

- В файле core.py хранятся основные константы приложения.
- Формат видео-файлов: .avi
- Формат файлов-аннотаций к видео: .txt
- Для корректного запуска приложения:
    - В папке data должны быть размещены 4 видео-файла.
    - В папке data должны быть размещены 4 файла-аннотации.
    - Название видео совпадает с названием аннотации.
    - Одна строка аннотации характеризует один кадр видеофайла.

## Автор, контактная информация:

Мартынова Валерия

- Email: emphoria@yandex.ru
- Telegram: @Emphori