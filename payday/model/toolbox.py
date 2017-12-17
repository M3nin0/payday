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
            creds = ServiceAccountCredentials.from_json_keyfile_name('google-secret/client_secret.json', scope)
            client = gspread.authorize(creds)
            # A tabela deverá ser alterada casa não siga o padrão do aplicativo
            tabela = client.open("faturas").sheet1
        except BaseException as e:
            print(e)
        return tabela
