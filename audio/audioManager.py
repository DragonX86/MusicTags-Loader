import re
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

from audio.trackModel import AudioTrack


class AudioManager:
    @staticmethod
    def get_track_list(m3u_file: Path):
        if not m3u_file.exists():
            raise FileNotFoundError

        track_num = 1

        with m3u_file.open('r') as file:
            for line in file:
                if line.startswith('#EXTINF:-1,'):
                    filename = " ".join(
                        line.strip()
                            .replace('#EXTINF:-1,', '')
                            .split()
                    )

                    yield filename, track_num
                    track_num += 1

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
    def found_file(download_path: Path, file_name: str) -> Path:
        # Функция для замены нескольких значений
        def multiple_replace(target_str, replaceable_values):
            # получаем заменяемое: подставляемое из словаря в цикле
            for i, j in replaceable_values.items():
                # меняем все target_str на подставляемое
                target_str = target_str.replace(i, j)
            return target_str

        # создаем словарь со значениями и строку, которую будет изменять
        replace_values = {
            '(': r'\(*',
            ')': r'\)*',
            '[': r'\[',
            ']': r'\]',
            chr(34): r'(")*',
            '$': r'\$*',
            '^': r'\^*',
            '.': r'\.*',
            '*': r'(\*)*',
            '+': r'(\+)*',
            '**': r'(\*\*)*',
            '..': r'(\.\.)*',
            '?': r'(\?)*',
            '!': r'(!)*',
            ':': r'(:|_)*',
            '/': r'(_)*',
        }

        # изменяем и печатаем строку
        file_name = f"^{multiple_replace(file_name, replace_values)}\\.*mp3$"

        for audio_file in download_path.glob('*.mp3'):
            if re.search(file_name, audio_file.name) is not None:
                return audio_file

    @staticmethod
    def rename_file(file_path: Path, track: AudioTrack):
        folder_path = file_path.parent

        new_name = f"{str(track.track_num).zfill(2)}. {track.title}.mp3"

        if "/" in new_name:
            new_name = new_name.replace('/', '_')

        file_path.rename(folder_path / new_name)

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
