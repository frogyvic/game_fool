import pathlib

from cutter import split_audio_by_silence_librosa
from youtubeCutter import split_youtube_video_by_silence
test_input_file=("C:/Users/vitoo/Desktop/a-calm-frutiger-aero-playlist.m4a")
test_output_file=("C:/Users/vitoo/Desktop/test")
# split_audio_by_silence_librosa(test_input_file,test_output_file)

split_youtube_video_by_silence("https://www.youtube.com/watch?v=lQz7RsVd-tQ",test_output_file)
