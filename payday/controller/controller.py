import os
import sys
import json

from model.interface import Menu
from model.toolbox import ToolBox
from model.interface import Faturas
from model.interface import Registro
from model.interface import Configuracao
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog

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
        self.menu.window.btn_sair.clicked.connect(lambda: exit())
        self.menu.window.btn_ver_faturas.clicked.connect(lambda: FaturasController())
        self.menu.window.btn_reg_faturas.clicked.connect(lambda: RegistroController())
        self.menu.window.action_configura.triggered.connect(lambda: ConfigController())

    def __init__(self):
        self.menu = Menu()

        # Configura funções nos botões
        self.__config_buttons()

        # Exibe o menu principal
        self.menu.window.show()
        sys.exit(self.menu.app.exec_())

class RegistroController(object):
    '''
        Controller dos registros de novas faturas
    '''

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
        '''
            Descrição
                Método para adicionar métodos aos botões
        '''
        self.dialog.reg.btn_registrar.clicked.connect(self.controla_registro)

    def __init__(self):

        self.dialog = Registro()

        # Configurando ação do botão
        self.__config_buttons()

        # Inicia o dialogo de registro
        self.dialog.reg.show()
        self.dialog.reg.exec_()

class ConfigController(object):

    def __save_config(self):
        '''
            Descrição
                Método que salva as informações inseridas pelo usuário no arquivos
                de configurações
        '''

        new_configs = {'config_api': []}
        new_configs['config_api'].append({'path_key': self.config.configure.input_path_api.toPlainText()})
        new_configs['config_api'].append({'name_sheet': self.config.configure.file_gdrive.toPlainText()})

        _file = 'config/config.json'

        if os.path.isfile(_file):
            os.remove(_file)

        try:
            with open(_file, 'w') as fil:
                json.dump(new_configs, fil)
                final = QMessageBox.information(self.config.configure, 'Sucesso',
                                            'Sucesso ao salvar as configurações')
        except:
            final = QMessageBox.critical(self.config.configure, 'Erro',
                                        'Erro ao tentar salvar as configurações')

    def __select_dir(self):
        '''
            Descrição
                Método que permite ao usuário selecionar o arquivo onde estão
                as chaves de autenticação do Google 
        '''
        self.client_secret = str(QFileDialog.getOpenFileName(
            self.config.configure, 'Seleção do arquivo chave do google'))

        if self.client_secret != '':
            self.config.configure.input_path_api.setText(self.client_secret[2:-19])

    def __config_buttons(self):
        '''
            Descrição
                Método para adicionar métodos aos botões
        '''
        self.config.configure.btn_select_file.clicked.connect(self.__select_dir)
        self.config.configure.btn_save.clicked.connect(self.__save_config)

    def __init__(self):
        self.client_secret = ''

        self.config = Configuracao()

        # Definindo as configurações nos campos caso exista
        if os.path.isfile('config/config.json'):
            config = ToolBox.load_config()

            if config != -1:
                self.config.configure.input_path_api.setText(config['config_api'][0]['path_key'])
                self.config.configure.file_gdrive.setText(config['config_api'][1]['name_sheet'])
            else:
                # Criando pré-definições
                self.config.configure.file_gdrive.setText('faturas')

        self.__config_buttons()
        self.config.configure.show()
        self.config.configure.exec_()

class FaturasController(object):
    def __init__(self):
        self.faturas = Faturas()

        # Inicia o dialogo de registro
        self.faturas.faturas.show()
        self.faturas.faturas.exec_()

class BotController(object):
    def __init__(self):
        pass
