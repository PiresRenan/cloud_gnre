from time import strftime, localtime
import datetime


class Create:
    def __init__(self):
        self.day = ''
        self.month = ''
        self.year = ''
        self.hour = ''
        self.minute = ''
        self.second = ''
        self.get_date()

    def get_date(self):
        data = localtime()
        self.day = strftime("%d", data)
        self.month = strftime("%m", data)
        self.year = strftime("%Y", data)
        self.hour = strftime("%H", data)
        self.minute = strftime("%M", data)
        self.second = strftime("%S", data)

    def is_business_day(self, target):
        # Verifica se a data é um dia útil (de segunda a sexta-feira)
        if target.weekday() < 5:
            return True
        return False

    def add_months(self, num_of_months):
        current_date = datetime.date.today()
        target_date = current_date + datetime.timedelta(days=num_of_months)
        while not self.is_business_day(target_date):
            target_date += datetime.timedelta(days=1)
        return target_date.strftime('%Y-%m-%d')

    def create_gnre(self, uf: str, ie_: str, valor_total: str, chave_nota: str) -> str:
        # SP, MT, RJ, AM, RN, AC, AL, BA, CE, DF, GO, MA, MG, MS, PA, PB, PE, PI, PR, RO, RR, RS, SC, SE
        string_final: str = ""
        if uf != 'SP' and uf != 'RJ':
            string_final: str = '<TDadosGNRE versao="2.00">'
            string_final += f'<ufFavorecida>{uf}</ufFavorecida>'
            string_final += '<tipoGnre>0</tipoGnre>'
            string_final += '<contribuinteEmitente>'
            string_final += '<identificacao>'
            string_final += '<CNPJ>62434436001703</CNPJ>'
            string_final += '</identificacao>'
            string_final += '<razaoSocial>CANDIDE INDUSTRIA E COMERCIO LTDA</razaoSocial>'
            string_final += '<endereco>RUA TEODORO SAMPAIO, 399 - CONJ. 57</endereco>'
            string_final += '<municipio>50308</municipio>'
            string_final += '<uf>SP</uf>'
            string_final += '<cep>05405000</cep>'
            string_final += '<telefone>1133260777</telefone>'
            string_final += '</contribuinteEmitente>'
            string_final += '<itensGNRE>'
            string_final += '<item>'
            string_final += '<receita>100099</receita>'

            if uf == 'MT':
                string_final += '<detalhamentoReceita>000105</detalhamentoReceita>'

            if uf == 'AC':
                string_final += '<detalhamentoReceita>000017</detalhamentoReceita>'

            if uf == 'TO':
                string_final += '<detalhamentoReceita>000005</detalhamentoReceita>'

            if uf == 'AC' or uf == 'AL' or uf == 'BA' or uf == 'AP' or uf == 'CE' or uf == 'DF' or uf == 'GO' or uf == 'MA' or uf == 'MG' or uf == 'MS' or uf == 'PA' or uf == 'PI' or uf == 'PR' or uf == 'RO' or uf == 'RR' or uf == 'SE' or uf == 'TO':
                string_final += f'<documentoOrigem tipo="10">{chave_nota[25:34]}</documentoOrigem>'

            if uf == 'AM' or uf == 'MT' or uf == 'PE' or uf == 'RS':
                string_final += f'<documentoOrigem tipo="22">{chave_nota[25:34]}</documentoOrigem>'

            elif uf == 'RJ' or uf == 'SC':
                string_final += f'<documentoOrigem tipo="24">{chave_nota}</documentoOrigem>'

            if uf == 'AM' or uf == 'BA' or uf == 'AC' or uf == 'CE' or uf == 'DF' or uf == 'MA' or uf == 'MS' or uf == 'PE' or uf == 'AL' or uf == 'GO' or uf == 'RR' or uf == 'TO':
                string_final += '<produto>44</produto>'

            if uf == 'AM' or uf == 'BA':
                string_final += '<referencia>'
                string_final += '<periodo>0</periodo>'
                string_final += f'<mes>{self.month}</mes>'
                string_final += f'<ano>{self.year}</ano>'
                string_final += '</referencia>'

            if uf == 'AC' or uf == 'DF' or uf == 'MA' or uf == 'RN' or uf == 'MT' or uf == 'GO' or uf == 'MG' or uf == 'PA' or uf == 'PB' or uf == 'RO' or uf == 'RR' or uf == 'SE' or uf == 'TO':
                string_final += '<referencia>'
                string_final += f'<mes>{self.month}</mes>'
                string_final += f'<ano>{self.year}</ano>'
                string_final += '</referencia>'

            if uf == 'AP':
                datav = self.add_months(1)
            else:
                datav = self.add_months(5)

            string_final += f'<dataVencimento>{datav}</dataVencimento>'
            string_final += f'<valor tipo="11">{valor_total}</valor>'

            if uf == 'RN':
                string_final += '<convenio>Bradesco</convenio>'

            if uf != "BA" or uf != 'DF' or uf != 'PR' or uf != 'SC':
                string_final += '<contribuinteDestinatario>'
                string_final += '<identificacao>'
                string_final += f'<IE>{str(int(ie_))}</IE>'
                string_final += '</identificacao>'
                string_final += '</contribuinteDestinatario>'

            if uf == 'MS':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>27</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'PB':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>30</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'RR':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>36</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'AP':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>47</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'AC':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>76</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'SE':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>77</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'TO':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>80</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'RO':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>83</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'AL':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>90</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'RN':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>97</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            if uf == 'GO':
                string_final += '<camposExtras>'
                string_final += '<campoExtra>'
                string_final += '<codigo>102</codigo>'
                string_final += f'<valor>{chave_nota}</valor>'
                string_final += '</campoExtra>'
                string_final += '</camposExtras>'

            string_final += '</item>'
            string_final += '</itensGNRE>'
            string_final += f'<valorGNRE>{valor_total}</valorGNRE>'
            string_final += f'<dataPagamento>{datav}</dataPagamento>'
            string_final += '</TDadosGNRE>'
        return string_final

    def create_xml(self, gnres: str) -> str:
        return f'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><TLote_GNRE xmlns="http://www.gnre.pe.gov.br" versao="2.00"><guias>{gnres}</guias></TLote_GNRE>'
