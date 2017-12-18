import json
import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ToolBox(object):
    @staticmethod
    def connect_to_drive():
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
        try:
            with open('config/config.json') as cfg:
                return json.load(cfg)
        except:
            return -1
