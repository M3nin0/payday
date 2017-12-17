import sys

from PyQt5.uic import loadUi
from model.toolbox import ToolBox
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
        total_row = len(self.tabela.get_all_values()) + 1
        try:
            novo_item = [
                total_row,
                self.get_emissao(),
                self.get_vencimento(),
                self.reg.input_empresa.toPlainText(),
                self.reg.input_valor.value(),
                self.reg.input_dias_aviso.value()
                ]
        except:
            return -1

        # Recuperando tabelas que serão preenchidas
        linha_tabela = self.tabela.range('A' + str(total_row) + ':' + 'F' + str(total_row))

        i = 0
        for key in linha_tabela:
            key.value = novo_item[i]
            i += 1

        try:
            self.tabela.update_cells(linha_tabela)
            return 1
        except:
            return -1

    def __init__(self):
        '''
            Descrição
                Método inicializador que carrega a interface do menu principal
        '''
        super(Registro, self).__init__()
        # Conecta com a api e devolve a interface de comunicaçãos
        self.tabela = ToolBox.connect_to_drive()
        # Carrega a interface gráfica
        self.reg = loadUi('view/registro.ui')
