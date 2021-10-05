import re
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

from utils.trackModel import AudioTrack


class AudioManager:
    @staticmethod
    def get_title(file_name: str):
        def __get_name(artists_part, title_part):
            if "feat" in artists_part:
                if "feat" not in title_part:
                    result = re.search(r'feat\. .*', artists_part)
                    return f"{title_part} ({result.group(0)})"
                else:
                    return title_part
            else:
                return name_part

        if file_name.count(' - ') > 1:
            artist_part = file_name.split(' - ')[0]
            name_part = ' - '.join(file_name.split(' - ')[1:])

            return __get_name(artist_part, name_part)
        else:
            artist_part, name_part = file_name.split(' - ')
            return __get_name(artist_part, name_part)

    @staticmethod
    def set_mp3_tags(file_path: Path, track: AudioTrack):
        audio = MP3(filename=str(file_path), ID3=EasyID3)

        audio['title'] = track.title
        audio['artist'] = track.artist
        audio['tracknumber'] = str(track.track_num)
        audio['date'] = track.year
        audio['album'] = track.album
        audio['genre'] = track.genre

        audio.save()

    @staticmethod
    def set_cover_image(file_path: Path, image_path: Path):
        audio = ID3(str(file_path))

        with open(image_path, 'rb') as album_art:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=album_art.read()
            )

        audio.save()
