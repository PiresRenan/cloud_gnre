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

    def send_gnre(self, path=None):
        recipient = 'contasareceber@candide.com.br'
        copy = ["suporte.renan@candide.com.br"]
        subject = "GNRE em lote"
        body = f'GNRE em lote em periodo de validação.'
        conf_path = path.split('\\')[1]
        binary_pdf = open('./temp/{}'.format(conf_path), 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=conf_path)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=self.pdf_name)

        msg = MIMEMultipart()
        msg.attach(payload)

        msg['From'] = self.username
        msg['To'] = recipient
        msg['Cc'] = ', '.join(copy)
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

