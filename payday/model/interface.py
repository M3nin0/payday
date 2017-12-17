import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog

class Menu(object):
    def __init__(self):
        '''
            Descrição
                Método inicializador que carrega a interface do menu principal
        '''
        # Carrega a interface
        self.app = QApplication(sys.argv)
        self.window = loadUi('view/menu.ui')

class Registro(QDialog):

    def registrar(self):
        pass

    def __init__(self):
        '''
            Descrição
                Método inicializador que carrega a interface do menu principal
        '''
        super(Registro, self).__init__()

        # Carrega a interface
        self.reg = loadUi('view/registro.ui')
