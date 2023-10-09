import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


class OutlookMailSender:

    def __init__(self, nota):
        self.recipient = "rafael@candide.com.br"
        self.copy = ["ronaldo@candide.com.br", "eliane@candide.com.br", "suporte.renan@candide.com.br",
                     "carlao@candide.com.br"]
        self.subject = f"Coleta {nota}."
        self.body = f'Coleta {nota}, segue o documento de confirmação em anexo.'
        self.username = "suporte.renan@candide.com.br"
        self.password = "02535040Rock;,"
        self.smtp_server = "smtp-mail.outlook.com"
        self.pdf_name = f"coleta_{nota}.pdf"

    def send_mail(self) -> bool:

        binary_pdf = open(self.pdf_name, 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=self.pdf_name)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=self.pdf_name)

        msg = MIMEMultipart()
        msg.attach(payload)

        msg['From'] = self.username
        msg['To'] = self.recipient
        msg['Cc'] = ', '.join(self.copy)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body))

        try:
            server = smtplib.SMTP(self.smtp_server, 587)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.close()
            return True
        except Exception as e:
            print(e)
            return False

    def send_gnre(self, path=None, info=None):
        if info is not None:
            edith = []
            jennefer = []
            noemia = []
            nao_cadastrado = []
            mensagem = """
As notas que possuem icmsSt e que estão prontas para o pagamento de seus impostos estão listados a seguir:
            """
            for nota in info:
                resp = nota.get('r')
                if resp == '18531':
                    edith.append(nota)
                elif resp == '9024':
                    jennefer.append(nota)
                elif resp == '9076':
                    noemia.append(nota)
                else:
                    nao_cadastrado.append(nota)
            if len(edith) > 0:
                str_e = ""
                for nota in edith:
                    str_e += "Numero da nota: {}\nNome do Cliente: {}\nUnidade Federativa: {}\nValor da Nota: {}\nLink para nota: {}\n --------------------------------------------------- \n".format(str(nota.get('chave_nota')).replace("000", ""), nota.get('n_cliente'), nota.get('uf'), nota.get('v_nota'), nota.get('nota_url'))
                edith_notas = """
As notas de EDITH ANA presentes no xml são {}, segue as informações delas: \n{}
""".format(len(edith), str_e)
                mensagem += edith_notas
            if len(jennefer) > 0:
                str_e = ""
                for nota in jennefer:
                    str_e += "Numero da nota: {}\nNome do Cliente: {}\nUnidade Federativa: {}\nValor da Nota: {}\nLink para nota: {}\n --------------------------------------------------- \n".format(str(nota.get('chave_nota')).replace("000", ""), nota.get('n_cliente'), nota.get('uf'), nota.get('v_nota'), nota.get('nota_url'))
                jennefer_notas = """
As notas de JENNEFER SOUZA presentes no xml são {}, segue as informações delas: \n{}
                """.format(len(jennefer), str_e)
                mensagem += jennefer_notas
            if len(noemia) > 0:
                str_e = ""
                for nota in noemia:
                    str_e += "Numero da nota: {}\nNome do Cliente: {}\nUnidade Federativa: {}\nValor da Nota: R$ {}\nLink para nota: {}\n --------------------------------------------------- \n".format(str(nota.get('chave_nota')).replace("000", ""), nota.get('n_cliente'), nota.get('uf'), nota.get('v_nota'), nota.get('nota_url'))
                noemia_notas = """
As notas de NOEMIA DA SILVA MAGALHAES presentes no xml são {}, segue as informações delas: \n{}
                """.format(len(noemia), str_e)
                mensagem += noemia_notas
            if len(nao_cadastrado) > 0:
                str_e = ""
                for nota in nao_cadastrado:
                    str_e += "Numero da nota: {}\nNome do Cliente: {}\nUnidade Federativa: {}\nValor da Nota: {}\nLink para nota: {}\n --------------------------------------------------- \n".format(str(nota.get('chave_nota')).replace("000", ""), nota.get('n_cliente'), nota.get('uf'), nota.get('v_nota'), nota.get('nota_url'))
                nao_cadastrado_notas = """
As notas de SEM CADASTRO NO NS presentes no xml são {}, segue as informações delas: \n{}
                """.format(len(nao_cadastrado), str_e)
                mensagem += nao_cadastrado_notas
                mensagem += """
\n\n
Atensiosamente,
Renan Pires.                
                """
        else:
            mensagem = "GNRE gerada"
        # recipient = 'financeiro@candide.com.br'
        recipient = 'suporte.renan@candide.com.br'
        # copy = ['suporte.renan@candide.com.br', 'contasareceber@candide.com.br']
        subject = "GNRE em lote"
        # body = "GNRE"
        body = mensagem
        try:
            conf_path = path.split('\\')[1]
        except:
            conf_path = path.split('/')[1]
        binary_pdf = open('./temp/{}'.format(conf_path), 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=conf_path)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=self.pdf_name)

        msg = MIMEMultipart()
        msg.attach(payload)

        msg['From'] = self.username
        msg['To'] = recipient
        # msg['Cc'] = ', '.join(copy)
        msg['Subject'] = subject
        msg.attach(MIMEText(body))

        try:
            server = smtplib.SMTP(self.smtp_server, 587)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.close()
            return True
        except Exception as e:
            print(e)
            return False

