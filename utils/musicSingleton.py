from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class MusicSingleton(metaclass=SingletonMeta):
    __artist: str = None
    __album_name: str = None
    __genre: str = None
    __year: str = None

    def get_artist(self):
        if self.__artist is None:
            raise ValueError('Не задано значение artist')

        return self.__artist

    def set_artist(self, artist: str):
        self.__artist = artist

    def get_album_name(self):
        if self.__album_name is None:
            raise ValueError('Не задано значение album_name')

        return self.__album_name

    def set_album_name(self, album_name: str):
        self.__album_name = album_name

    def get_genre(self):
        if self.__genre is None:
            raise ValueError('Не задано значение genre')

        return self.__genre

    def set_genre(self, genre: str):
        self.__genre = genre

    def get_year(self):
        if self.__year is None:
            raise ValueError('Не задано значение year')

        return self.__year

    def set_year(self, year: str):
        self.__year = year
