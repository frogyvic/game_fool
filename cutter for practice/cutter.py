import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

import librosa
import soundfile as sf
import numpy as np
import os
import time
from datetime import datetime

def format_time(track_num):
    time_str = datetime.now().strftime("%d-%H-%M-%S")
    return f"track_{track_num:02d}_{time_str}.wav"

def split_audio_by_silence_librosa(input_file, output_folder="splitted_tracks",
                                   min_silence_duration=0.4,  #минимальная длительность тишины в сек.
                                   silence_thresh_db=-40,  # порог тишины(0-максимальная громкость, уходит в отрицательное число)
                                   min_track_duration=30,  # мин. длительность трека в сек.
                                   keep_silence=1,  # тишина по краям
                                   keep_start=True):  # сохранять начало файла

    print(f"Загрузка файла: {input_file}")
    audio, sr = librosa.load(input_file, sr=None, mono=False)
    start_time = time.time()
    #анализ
    if len(audio.shape) > 1:
        audio_mono = np.mean(audio, axis=0)
    else:
        audio_mono = audio
    # Анализ RMS энергии
    hop_length = 512
    frame_length = 2048
    rms = librosa.feature.rms(y=audio_mono, frame_length=frame_length, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)

    # Находим тишину
    is_silence = rms_db < silence_thresh_db

    # Находим индексы тишины
    silence_start_idx = []
    silence_end_idx = []
    in_silence = False
    for i, silence in enumerate(is_silence):
        if silence and not in_silence:
            silence_start_idx.append(i)
            in_silence = True
        elif not silence and in_silence:
            silence_end_idx.append(i)
            in_silence = False
    # Конвертируем в секунды
    times = librosa.frames_to_time(np.arange(len(is_silence)), sr=sr, hop_length=hop_length)
    # Интервалы тишины
    silence_intervals = []
    for start_idx, end_idx in zip(silence_start_idx, silence_end_idx):
        duration = times[end_idx] - times[start_idx]
        if duration >= min_silence_duration:
            silence_intervals.append((times[start_idx], times[end_idx]))

    print(f" Найдено {len(silence_intervals)} участков тишины длительностью от {min_silence_duration} сек")
    # Определяем границы треков
    duration = len(audio_mono) / sr if len(audio.shape) == 1 else audio.shape[1] / sr
    # Сначала находим ВСЕ возможные треки (включая короткие)
    raw_track_boundaries = []
    if keep_start:
        last_end = 0
        for start, end in silence_intervals:
            if start > last_end:
                raw_track_boundaries.append((last_end, start))
            last_end = end
        if duration > last_end:
            raw_track_boundaries.append((last_end, duration))
    else:
        last_end = 0
        for start, end in silence_intervals:
            if start - last_end >= min_track_duration:
                raw_track_boundaries.append((last_end, start))
            last_end = end
        if duration - last_end >= min_track_duration:
            raw_track_boundaries.append((last_end, duration))

    print(f" Найдено {len(raw_track_boundaries)} сырых треков (включая короткие)")

    # ОБЪЕДИНЯЕМ короткие треки со следующим
    track_boundaries = []
    i = 0
    while i < len(raw_track_boundaries):
        current_start, current_end = raw_track_boundaries[i]
        current_duration = current_end - current_start

        # Если трек достаточно длинный или это последний трек
        if current_duration >= min_track_duration or i == len(raw_track_boundaries) - 1:
            track_boundaries.append((current_start, current_end))
            i += 1
        else:
            # Короткий трек - присоединяем к следующему
            # Ищем следующий трек для присоединения
            next_start, next_end = raw_track_boundaries[i + 1]
            # Присоединяем текущий короткий трек к следующему
            merged_end = next_end
            merged_start = current_start
            merged_duration = merged_end - merged_start

            # Заменяем текущий и следующий на объединённый
            raw_track_boundaries[i] = (merged_start, merged_end)
            # Удаляем следующий трек
            raw_track_boundaries.pop(i + 1)
            # Не увеличиваем i, проверяем объединённый трек заново
            print(f"   🔗 Присоединён короткий трек ({current_duration:.1f} сек) к следующему")

    print(f" После объединения: {len(track_boundaries)} треков")

    # Создаем папку
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Сохраняем треки
    saved_tracks = []
    for i, (start_time_track, end_time_track) in enumerate(track_boundaries, start=1):
        start_sample = int(start_time_track * sr)
        end_sample = int(end_time_track * sr)

        # Вырезаем трек
        if len(audio.shape) == 1:  # Моно
            track = audio[start_sample:end_sample]
        else:  # Стерео
            track = audio[:, start_sample:end_sample].T

        # Добавляем тишину по краям
        if keep_silence > 0:
            silence_samples = int(keep_silence * sr)
            if len(audio.shape) == 1:  # Моно
                silence_pad = np.zeros(silence_samples)
                track = np.concatenate([silence_pad, track, silence_pad])
            else:  # Стерео
                silence_pad = np.zeros((silence_samples, track.shape[1]))
                track = np.concatenate([silence_pad, track, silence_pad])

        # Сохраняем


        output_file = os.path.join(output_folder, format_time(i))
        sf.write(output_file, track, sr)
        track_duration = len(track) / sr
        print(
            f"✅ Трек {i}: {os.path.basename(output_file)} (длительность: {track_duration:.1f} сек, начинается с {start_time_track:.1f} сек)")
        saved_tracks.append(output_file)

    end_time = time.time()
    print(f"\n✨ Готово! Сохранено {len(saved_tracks)} треков в папку '{output_folder}'")
    print(f"⏱️ Общее время обработки: {end_time - start_time:.1f} секунд")
    print(saved_tracks)
    return saved_tracks
