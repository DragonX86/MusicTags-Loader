from pathlib import Path

from PyQt5.QtCore import pyqtSignal, QObject

from audio.audioManager import AudioManager
from audio.musicSingleton import MusicSingleton
from audio.trackModel import AudioTrack


class AudioWorker(QObject):
    finished = pyqtSignal()

    def __init__(self,
                 album_folder_path: Path,
                 cover_album_path: Path,
                 m3u_file: Path):
        super().__init__()

        self.album_folder = album_folder_path
        self.cover_album = cover_album_path
        self.m3u_file = m3u_file

    def run(self):
        for name, track_number in AudioManager.get_track_list(self.m3u_file):
            file = AudioManager.found_file(self.album_folder, name)

            music_info = MusicSingleton()

            audio_track = AudioTrack(
                track_num=track_number,
                title=AudioManager.get_title(name),
                artist=music_info.get_artist(),
                album=music_info.get_album_name(),
                genre=music_info.get_genre(),
                year=music_info.get_year()
            )

            AudioManager.set_mp3_tags(file, audio_track)

            AudioManager.set_cover_image(file, self.cover_album)
            AudioManager.rename_file(file, audio_track)

            print(file)
