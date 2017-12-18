import json
import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ToolBox(object):
    '''
        Classe com métodos úteis para o funcionamento do programa
    '''
    @staticmethod
    def connect_to_drive():
        '''
            Descrição
                Método para abrir a conexão entre o cliente e o google drive
        '''
        # Acesso feito utilizando o tutorial:
        # goo.gl/sf4BNr
        scope = ['https://spreadsheets.google.com/feeds']
        # a chave api deve ser substituida para o app do usuário
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(ToolBox.load_config()['config_api'][0]['path_key'], scope)
            client = gspread.authorize(creds)
            # A tabela deverá ser alterada casa não siga o padrão do aplicativo
            tabela = client.open(ToolBox.load_config()['config_api'][1]['name_sheet']).sheet1
        except BaseException as e:
            print(e)
        return tabela

    @staticmethod
    def load_config():
        '''
            Descrição
                Método que recupera as informações do arquivo de configuração
        '''
        try:
            with open('config/config.json') as cfg:
                return json.load(cfg)
        except:
            return -1
