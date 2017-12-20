import os
import sys
import json

import numpy as np
import pandas as pd

from model.interface import Menu
from time import gmtime, strftime
from model.toolbox import ToolBox
from bokeh.layouts import gridplot
from model.interface import Faturas
from model.interface import Registro
from model.interface import Configuracao
from bokeh.plotting import figure, output_file, show
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
        self.menu.window.btn_ver_relatorio.clicked.connect(lambda: ReportController())
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

class ReportController(object):
    def __init__(self):
        actual_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

        file_name = 'report/' + actual_time + '.html'

        output_file(file_name)

        table = ToolBox.connect_to_drive()

        faturas_itens = pd.DataFrame(table.get_all_values()[1:])

        faturas_itens.columns = ['fatura_id', 'emissao', 'vencimento',
        'empresa', 'valor', 'dias_aviso', 'status']

        a_pagar = faturas_itens[faturas_itens['status'] == 'Em aberto']
        fechados = faturas_itens[faturas_itens['status'] == 'Fechado']
        arange = np.arange(len(a_pagar['valor']))
        arange_2 = np.arange(len(fechados['valor']))

        # Plota gráfico com valor das faturas em aberto
        plot = figure(plot_width=700, plot_height=700, title='Valor das compras (Em aberto)')
        plot.line(arange, a_pagar['valor'], line_width=4)

        plot_2 = figure(plot_width=700, plot_height=700, title='Faturas abertas X fechadas')

        if len(a_pagar['valor']) > 0:
            init = 1
            final = len(a_pagar['valor'])
        else:
            init = 0
            final = 0

        if len(fechados['valor']) > 0:
            init_2 = 1
            final_2 = len(fechados['valor']) + 1
        else:
            init_2 = 0
            final_2 = 0

        plot_2.multi_line([arange, np.arange(init, final)], [arange, np.arange(init_2, final_2)],
             color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        grid = gridplot([[plot, plot_2]])

        show(grid)

class BotController(object):
    def __init__(self):
        pass
