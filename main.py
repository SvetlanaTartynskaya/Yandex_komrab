import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests

STATIC_API_SERVER = "https://static-maps.yandex.ru/1.x/"


def get_map_from_coords(coords, type_in=str):
    params = {
        "ll": coords if type_in is str else ",".join(coords),
        "spn": "0.05,0.05",
        "l": "map"
    }

    res = requests.request(method="GET", url=STATIC_API_SERVER, params=params)

    if res.status_code == 200:
        return res.content
    return None


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt.ui', self)
        self.search_btn.clicked.connect(self.search)

    def search(self):
        coords = (self.line_enter_coords.text().replace(" ", "").split(","))
        image = get_map_from_coords(coords, type_in=list)
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        self.map.setPixmap(pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())