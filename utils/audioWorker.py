from pathlib import Path

from PyQt5.QtCore import pyqtSignal, QObject
from utils.musicSingleton import MusicSingleton
from utils.trackModel import AudioTrack
from utils.audioManager import AudioManager
from utils.fileManager import (
    get_track_list,
    found_file,
    rename_file
)


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
        error_list = list()

        for number, name in enumerate(get_track_list(self.m3u_file), 1):
            file = found_file(self.album_folder, name)

            if file is not None:
                music_info = MusicSingleton()

                audio_track = AudioTrack(
                    track_num=number,
                    title=AudioManager.get_title(name),
                    artist=music_info.get_artist(),
                    album=music_info.get_album_name(),
                    genre=music_info.get_genre(),
                    year=music_info.get_year()
                )

                AudioManager.set_mp3_tags(file, audio_track)
                AudioManager.set_cover_image(file, self.cover_album)

                rename_file(file, audio_track)
            else:
                error_list.append(name)

        if len(error_list) != 0:
            print(error_list)
        else:
            self.finished.emit()
