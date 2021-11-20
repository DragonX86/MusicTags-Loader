#!/usr/bin/env python3
import sys
from pathlib import Path

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from utils.musicSingleton import MusicSingleton
from utils.audioWorker import AudioWorker

mp3_genre = ["Rap", "Rock"]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = uic.loadUiType('main.ui')[0]()
        self.ui.setupUi(self)

        self.folder_selected = False
        self.folder_path = Path.home() / 'Музыка'

        self.cover_selected = False
        self.cover_path = None

        self.m3u_selected = False
        self.m3u_file = None

        self.ui.genre_combobox.addItems(mp3_genre)
        self.ui.folderAlbum_button.clicked.connect(self.folderAlbum_button_click)
        self.ui.coverAlbum_button.clicked.connect(self.coverAlbum_button_click)
        self.ui.m3u_button.clicked.connect(self.m3u_button_click)

        self.ui.result_button.clicked.connect(self.result_button_click)

    def folderAlbum_button_click(self):
        folder = QFileDialog.getExistingDirectory(None, 'Выберите папку с альбомом', str(Path.home() / 'Музыка'))
        self.ui.folderAlbum_lineEdit.setText(folder)

        self.folder_path = Path(folder)
        self.folder_selected = True

    def coverAlbum_button_click(self):
        files_filter = "JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png)"
        cover = QFileDialog.getOpenFileName(None, 'Select a image', str(self.folder_path), files_filter)
        self.ui.coverAlbum_lineEdit.setText(cover[0])

        self.cover_path = Path(cover[0])
        self.cover_selected = True

    def m3u_button_click(self):
        file_filter = "M3U (*.m3u)"
        m3u_file = QFileDialog.getOpenFileName(None, 'Select a m3u file', str(Path.home() / 'Загрузки'), file_filter)
        self.ui.m3u_lineEdit.setText(m3u_file[0])

        self.m3u_file = Path(m3u_file[0])
        self.m3u_selected = True

    def result_button_click(self):
        if self.m3u_selected:
            music_info = MusicSingleton()

            music_info.set_artist(self.ui.artistAlbum_lineEdit.text())
            music_info.set_album_name(self.ui.nameAlbum_lineEdit.text())
            music_info.set_genre(self.ui.genre_combobox.currentText())
            music_info.set_year(self.ui.yearAlbum_lineEdit.text())

            self.thread = QThread()

            self.worker = AudioWorker(
                album_folder_path=self.folder_path,
                cover_album_path=self.cover_path,
                m3u_file=self.m3u_file
            )

            self.worker.moveToThread(self.thread)

            self.worker.finished.connect(self.finished_signal_handler)

            self.thread.started.connect(self.worker.run)
            self.thread.start()

    @pyqtSlot()
    def finished_signal_handler(self):
        msgBox = QMessageBox()

        msgBox.setWindowTitle("Сообщение о завершении")
        msgBox.setText("Все файлы успешно обработаны!")

        msgBox.exec()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
