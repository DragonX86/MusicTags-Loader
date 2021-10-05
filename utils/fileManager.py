import re
from pathlib import Path

from utils.trackModel import AudioTrack


def get_track_list(m3u_file: Path):
    if not m3u_file.exists():
        raise FileNotFoundError

    with open(m3u_file, mode='r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('#EXTINF:-1,'):
                filename = " ".join(
                    line.strip()
                        .replace('#EXTINF:-1,', '')
                        .split()
                )

                yield filename


def found_file(download_path: Path, file_name: str) -> Path:
    # функция для замены нескольких значений
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
        '[': r'\[*',
        ']': r'\]*',
        '*': r'(\*)*',
        '+': r'(\+)*',
        chr(34): r'(")*',
        '$': r'\$*',
        '^': r'\^*',
        '.': r'\.*',
        '?': r'(\?)*',
        '!': r'(!)*',
        ':': r'(:|_)*',
        '/': r'(_)*',
    }

    for audio_file in download_path.glob('*.mp3'):
        if re.search(multiple_replace(file_name, replace_values), audio_file.stem) is None:
            continue
        return audio_file


def rename_file(file_path: Path, track: AudioTrack):
    folder_path = file_path.parent

    new_name = f"{str(track.track_num).zfill(2)}. {track.title}.mp3"

    if "/" in new_name:
        new_name = new_name.replace('/', '_')

    file_path.rename(folder_path / new_name)
