from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSignal

class loadPls(QObject):
    loaded=pyqtSignal(int,int)
    def load(self):
        self.loaded.emit(3, 5)

@pyqtSlot(int,int)
def on_loaded(x,y):
    print('hi')
    print(x)
    print(y)

Run=loadPls()
Run.loaded.connect(on_loaded)
Run.load()
