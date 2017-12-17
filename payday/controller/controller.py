import sys

from model.interface import Menu
from model.interface import Registro
from PyQt5.QtWidgets import QMessageBox, QDialog

class MenuController(object):
    '''
        Controller do menu inicial e suas funcionalidades
    '''
    def __config_buttons(self):
        '''
            Descrição
                Método para realizar a configuração das funções em cada botão
                do menu principal
        '''
        self.menu.window.btn_reg_faturas.clicked.connect(lambda: RegistroController())
        self.menu.window.btn_ver_faturas.clicked.connect(lambda: FaturasController())
        self.menu.window.btn_sair.clicked.connect(lambda: exit())

    def __init__(self):
        self.menu = Menu()

        # Configura funções nos botões
        self.__config_buttons()

        # Exibe o menu principal
        self.menu.window.show()
        sys.exit(self.menu.app.exec_())

class RegistroController(object):

    def controla_registro(self):
        '''
            Descrição
                Método que faz as verificações de campos preenchidos para que depois
                o registro possa ser feito
        '''

        invalido = False
        # Realiza verificações de validade nos campos
        if self.dialog.reg.input_empresa.toPlainText().replace(' ', '') == '':
            invalido = True
        elif self.dialog.reg.input_valor.value() == 0:
            invalido = True

        if invalido:
            msg = QMessageBox.warning(self.dialog.reg, 'Campos inválidos',
                                        'Todos os campos devem ser preenchidos')

        result = self.dialog.registrar()

        if result >= 0:
            resultado = QMessageBox.information(self.dialog.reg, 'Sucesso',
                                        'Os dados foram salvos com sucesso!')
        else:
            resultado = QMessageBox.critical(self.dialog.reg, 'Erro',
                                        'Erro ao tentar salvar os dados')

        self.dialog.reg.close()

    def __config_buttons(self):
        self.dialog.reg.btn_registrar.clicked.connect(self.controla_registro)

    def __init__(self):

        self.dialog = Registro()

        # Configurando ação do botão
        self.__config_buttons()

        # Inicia o dialogo de registro
        self.dialog.reg.show()
        self.dialog.reg.exec_()

class FaturasController(object):
    def __init__(self):
        pass

class BotController(object):
    def __init__(self):
        pass
