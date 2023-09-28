import json
from datetime import date, datetime

from .connection import NS_Services


class Coleta_methods(NS_Services):
    def get_NFE(self, NFe: str) -> dict:
        payload = {
            "q": f"SELECT customer.companyname AS customer_name, "
                 f"transaction.custbody_enl_accesskey AS nfe_, "
                 f"transaction.custbody_enl_volumesqty AS qtd, "
                 f"transaction.custbody_enl_fiscaldocdate AS data_nota, "
                 f"transportadora.name AS transportadora, "
                 f"FROM transaction "
                 f"FULL JOIN customer ON customer.id = transaction.entity "
                 f"FULL JOIN customrecord_enl_transportadoras AS transportadora ON transportadora.id = transaction.custbody_enl_carrierid "
                 f"WHERE custbody_enl_accesskey='{NFe}'"

        }
        result = self.get_results(1, "POST", "", payload)
        try:
            result = result.json()
        except Exception as e:
            result = {"items": [{"customer_name": "", "nfe_": "", "qtd": "", "transportadora": "", "data_nota": ""}]}
        try:
            cliente: str = result['items'][0]['customer_name']
        except Exception as e:
            cliente: str = ""
        try:
            n_nota: int = int(result['items'][0]['nfe_'][25:-10])
        except Exception as e:
            n_nota: int = 0
        try:
            qtd_ = result['items'][0]['qtd']
        except Exception as e:
            qtd_ = ""
        try:
            transport = result['items'][0]['transportadora']
        except Exception as e:
            transport = ""
        try:
            data_emissao_ = result['items'][0]['data_nota']
        except Exception as e:
            data_emissao_ = ""
        coleta: dict = {"cliente": cliente, "numero_nota": n_nota, "quantidade": qtd_, "transportadora": transport,
                        "data_emissao": data_emissao_}
        return coleta

    def get_NFE_from_expedition(self, NFe: str):
        payload = {
            "q": f"SELECT custrecord1462 FROM customrecord_can_expedicao WHERE custrecord1462={NFe}"
        }
        result = self.get_results(1, "POST", "", payload)
        try:
            result = result.json()
        except Exception as e:
            result = {"count": 0}
        if result["count"] > 0:
            return False
        else:
            return True

    def get_motoristas(self) -> list:
        payload = {
            "q": "SELECT name FROM CUSTOMRECORD_CAN_MOTORISTAS"
        }
        result = self.get_results(1, "POST", "", payload)
        try:
            result = result.json()
        except Exception as e:
            result = {"items": {"name": 0}}
        drivers: list = [""]
        for driver in result['items']:
            drivers.append(driver['name'])
        return drivers

    def get_cars(self):
        payload = {
            "q": "SELECT name FROM customrecord182"
        }
        result = self.get_results(1, "POST", "", payload)
        try:
            result = result.json()
        except Exception as e:
            print(e)
            result = ""
        cars: list = [""]
        for car in result['items']:
            cars.append(car['name'])
        return cars

    def insert_exp(self, coleta_number, cliente, nro_nfe, volume_, motorista, carro,
                   obs, _transportadora, data_emissao):
        url_ = "https://7586908.suitetalk.api.netsuite.com/services/rest/record/v1/CUSTOMRECORD_CAN_EXPEDICAO/"
        dia = date.today().day
        mes = date.today().month
        ano = date.today().year
        date_1 = datetime(ano, mes, dia)
        date_string = date_1.strftime('%Y-%m-%d')
        _data_emissao = datetime.strptime(data_emissao, "%d/%m/%Y")
        _data_emissao = _data_emissao.strftime("%Y-%m-%d")
        payload = {
            "custrecord1462": nro_nfe,
            "custrecord1463": _data_emissao,
            "custrecord1464": date_string,
            "custrecord1465": cliente,
            "custrecord1466": int(volume_),
            "custrecord1467": carro,
            "custrecord1468": motorista,
            "custrecord1469": coleta_number,
            "custrecord1470": obs,
            "custrecord1471": _transportadora,
        }

        result = self.get_results(1, "POST", url_, payload)
        return result.text

    def get_lastOne(self):
        url_ = "https://7586908.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql?limit=1"
        payload = {
            "q": "SELECT MAX(custrecord1469)+1 FROM customrecord_can_expedicao"
        }
        result = (self.get_results(1, "POST", url_, payload)).json()
        result = int(result["items"][0]["expr1"])
        return result
