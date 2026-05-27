import yt_dlp
import os
import tempfile
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np
import time
from datetime import datetime
from cutter import split_audio_by_silence_librosa


def format_time(track_num):
    time_str = datetime.now().strftime("%d-%H-%M-%S")
    return f"track_{track_num:02d}_{time_str}.wav"


def download_audio_from_youtube(youtube_url, output_path):
    """
    Скачивает аудио из YouTube видео во временную папку.
    Возвращает путь к скачанному файлу.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Скачиваем в WAV для совместимости
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,  # Убираем лишний вывод
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        # Получаем путь к скачанному файлу
        downloaded_file = ydl.prepare_filename(info).replace('.webm', '.wav').replace('.m4a', '.wav')
        return downloaded_file


def split_youtube_video_by_silence(youtube_url, output_folder="splitted_tracks",
                                   min_silence_duration=0.4,
                                   silence_thresh_db=-40,
                                   min_track_duration=30,
                                   keep_silence=1,
                                   keep_start=True):
    """
    Анализирует и нарезает аудио из YouTube видео на треки.
    """
    print(f"Обработка YouTube видео: {youtube_url}")

    #временная папка для аудио
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Скачивание аудио во временную папку: {temp_dir}")

        #скачиваем аудио
        try:
            audio_file_path = download_audio_from_youtube(youtube_url, temp_dir)
            print(f"Аудио успешно скачано: {audio_file_path}")
        except Exception as e:
            print(f"Ошибка при скачивании видео: {e}")
            return []

        #режем аудио с помощью имеющейся функции
        return split_audio_by_silence_librosa(
            input_file=audio_file_path,
            output_folder=output_folder,
            min_silence_duration=min_silence_duration,
            silence_thresh_db=silence_thresh_db,
            min_track_duration=min_track_duration,
            keep_silence=keep_silence,
            keep_start=keep_start
        )