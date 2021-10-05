from dataclasses import dataclass


@dataclass
class AudioTrack:
    title: str
    artist: str
    album: str
    track_num: int
    genre: str
    year: str
