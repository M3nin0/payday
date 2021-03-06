import sys

from PyQt5.uic import loadUi
from model.toolbox import ToolBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate, QLocale
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QMessageBox

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
    '''
        Classe da interface de registro de faturas
    '''

    def get_emissao(self):
        '''
            Descrição
                Método que devolve a data de emissão da fatura já formatada
        '''
        return QLocale(QLocale.Portuguese, QLocale.Brazil).toString(self.reg.date_emissao.date(), 'dd-MM-yyyy')

    def get_vencimento(self):
        '''
            Descrição
                Método que devolve a data de vencimento da fatura já formatada
        '''
        return QLocale(QLocale.Portuguese, QLocale.Brazil).toString(self.reg.date_vencimento.date(), 'dd-MM-yyyy')

    def registrar(self):
        '''
            Descrição
                Método que salva a nova fatura inserida pelo usuário
        '''
        total_row = len(self.tabela.get_all_values()) + 1
        try:
            novo_item = [
                total_row,
                self.get_emissao(),
                self.get_vencimento(),
                self.reg.input_empresa.toPlainText(),
                self.reg.input_valor.value(),
                self.reg.input_dias_aviso.value(),
                'Em aberto'
                ]
        except:
            return -1

        # Recuperando tabelas que serão preenchidas
        linha_tabela = self.tabela.range('A' + str(total_row) + ':' + 'G' + str(total_row))

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
                Método inicializador que carrega a interface do dialogo de registro
        '''
        super(Registro, self).__init__()
        # Conecta com a api e devolve a interface de comunicaçãos
        self.tabela = ToolBox.connect_to_drive()
        # Carrega a interface gráfica
        self.reg = loadUi('view/registro.ui')

class Configuracao(QDialog):
    '''
        Classe da interface de configurações do programa
    '''
    def __init__(self):
        super(Configuracao, self).__init__()

        self.configure = loadUi('view/configuracao.ui')

class Faturas(QDialog):
    '''
        Classe da interface de visualização de faturas registradas
    '''

    def fechar_fatura(self):
        '''
            Descrição
                Método para realizar a mudança de status da fatura selecionada
                pelo usuário
        '''
        id_alterada = self.faturas.faturas.currentItem().text()[4]

        for fatura in self.faturas_itens:
            if fatura[0] == id_alterada:
                fatura[6] = 'Fechado'

        self.tabela.update_acell('G' + id_alterada, 'Fechado')
        self.faturas.faturas.clear()
        self.__preenche_campo()

    def visualiza_infos(self):
        id_atual = self.faturas.faturas.currentItem().text()[4]

        if self.faturas_itens != []:
            for fatura in self.faturas_itens:
                if id_atual == fatura[0]:
                    resultado = QMessageBox.information(self.faturas, 'Detalhes',
                                    'Data de emissão: ' + fatura[1] +
                                    '\nData de vencimento: ' + fatura[2] +
                                    '\nNome da empresa: ' + fatura[3] +
                                    '\nValor da conta: ' + fatura[4] +
                                    '\nStatus da fatura: ' + fatura[6])

    def __preenche_campo(self):
        '''
            Descrição
                Este método preenche o QListWidgets com os dados recuperados do
                Google SpreadSheets
        '''
        try:
            self.faturas_itens = self.tabela.get_all_values()[1:]
        except BaseException as e:
            print(e)

        for fatura in self.faturas_itens:
            self.faturas.faturas.addItem(
            'ID: ' + fatura[0] + ' | ' + fatura[3] + ' - Vencimento: ' + fatura[2] + ' | Status: ' + fatura[6]
            )

    def __init__(self):
        super(Faturas, self).__init__()

        self.faturas = loadUi('view/faturas.ui')
        # Conecta com a api e devolve a interface de comunicaçãos
        self.tabela = ToolBox.connect_to_drive()

        self.faturas.btn_view.clicked.connect(self.visualiza_infos)
        self.faturas.fechar_fatura.clicked.connect(self.fechar_fatura)

        self.faturas_itens = []
        self.__preenche_campo()
