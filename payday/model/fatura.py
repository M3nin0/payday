class Fatura(object):
    def __init__(self, emissao, vencimento, empresa, valor, dias_aviso):
        self.emissao = emissao
        self.vencimento = vencimento
        self.empresa = empresa
        self.valor = valor
        self.dias_aviso = dias_aviso
