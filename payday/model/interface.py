import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate, QLocale
from PyQt5.QtWidgets import QApplication

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

    def get_emissao(self):
        return QLocale(QLocale.Portuguese, QLocale.Brazil).toString(self.reg.date_emissao.date(), 'dd-MM-yyyy')

    def get_vencimento(self):
        return QLocale(QLocale.Portuguese, QLocale.Brazil).toString(self.reg.date_vencimento.date(), 'dd-MM-yyyy')

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
