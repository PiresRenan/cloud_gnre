import requests

from gerador_de_lotes_gnre import cd
from .connection import NS_Services


class Gerador_Methods(NS_Services):

    def get_NFE(self, data_comeco: str, data_limite: str):
        result = []
        payload = {
            "q": f"SELECT "
                 f"t.id AS id_doc_fiscal, "
                 f"t.createdby AS criado_apartir_de, "
                 f"t.custbody_avlr_document_code AS nf_avalara_code, "
                 f"t.custbody_enl_linknotafiscal AS url_nf, "
                 f"t.trandate AS data_da_nota, "
                 f"t.custbody_enl_fiscaldocnumber AS n_nf, "
                 f"t.custbody_can_gerougnreemlote AS flag, "
                 f"t.custbody_enl_accesskey AS key_value, "
                 f"c.custentity_enl_cnpjcpf AS cnpj, "
                 f"c.companyname AS cliente, "
                 f"c.id AS ns_id, "
                 f"c.custentity_enl_legalname AS razao_social, "
                 f"c.custentity_enl_ienum AS ie_cliente, "
                 f"c.custentitycan_ufcli_paragnre AS uf, "
                 f"SUM(tx_trans.custrecord_enl_taxamount) AS total_ICMSTS "
                 f"FROM "
                 f"transaction AS t LEFT JOIN customer AS c ON c.id=t.entity LEFT JOIN customrecord_enl_taxtrans AS tx_trans ON tx_trans.custrecord_enl_tt_orderid=t.id "
                 f"WHERE "
                 f"t.trandate >= '{ data_comeco }' AND t.trandate >= '{ data_limite }' AND "
                 f"t.type = 'CustInvc' AND t.approvalstatus = '2' AND "
                 f"tx_trans.custrecord_enl_taxcode = 'icmsSt' AND t.custbody_can_gerougnreemlote = 'F' AND "
                 f"c.custentitycan_ufcli_paragnre!='SP' AND c.custentitycan_ufcli_paragnre!='RJ' "
                 f"GROUP BY "
                 f"t.id, t.createdby, t.custbody_avlr_document_code, t.custbody_enl_linknotafiscal, t.custbody_enl_fiscaldocnumber, "
                 f"t.trandate, t.custbody_can_gerougnreemlote, t.custbody_enl_accesskey, c.custentity_enl_cnpjcpf, c.companyname, "
                 f"c.id, c.custentity_enl_legalname, c.custentity_enl_ienum, c.custentitycan_ufcli_paragnre"
        }
        nf_info = self.get_results(1, "POST", "", payload)
        nf_info = nf_info.json()
        for nf in nf_info['items']:
            del nf['links']
            result.append(nf)
        return result

    def get_NFE_unique(self, nf_number=None):
        result = []
        payload = {
            "q": f"SELECT "
                 f"t.id AS id_doc_fiscal, "
                 f"t.createdby AS criado_apartir_de, "
                 f"t.custbody_avlr_document_code AS nf_avalara_code, "
                 f"t.custbody_enl_linknotafiscal AS url_nf, "
                 f"t.trandate AS data_da_nota, "
                 f"t.custbody_enl_fiscaldocnumber AS n_nf, "
                 f"t.custbody_can_gerougnreemlote AS flag, "
                 f"t.custbody_enl_accesskey AS key_value, "
                 f"c.custentity_enl_cnpjcpf AS cnpj, "
                 f"c.companyname AS cliente, "
                 f"c.id AS ns_id, "
                 f"c.custentity_enl_legalname AS razao_social, "
                 f"c.custentity_enl_ienum AS ie_cliente, "
                 f"c.custentitycan_ufcli_paragnre AS uf, "
                 f"SUM(tx_trans.custrecord_enl_taxamount) AS total_ICMSTS "
                 f"FROM "
                 f"transaction AS t LEFT JOIN customer AS c ON c.id=t.entity LEFT JOIN customrecord_enl_taxtrans AS tx_trans ON tx_trans.custrecord_enl_tt_orderid=t.id "
                 f"WHERE "
                 f"t.custbody_enl_fiscaldocnumber = '{ nf_number }' AND "
                 f"t.type = 'CustInvc' AND t.approvalstatus = '2' AND "
                 f"tx_trans.custrecord_enl_taxcode = 'icmsSt' AND "
                 f"c.custentitycan_ufcli_paragnre!='SP' AND c.custentitycan_ufcli_paragnre!='RJ' "
                 f"GROUP BY "
                 f"t.id, t.createdby, t.custbody_avlr_document_code, t.custbody_enl_linknotafiscal, t.custbody_enl_fiscaldocnumber, "
                 f"t.trandate, t.custbody_can_gerougnreemlote, t.custbody_enl_accesskey, c.custentity_enl_cnpjcpf, c.companyname, "
                 f"c.id, c.custentity_enl_legalname, c.custentity_enl_ienum, c.custentitycan_ufcli_paragnre"
        }
        nf_info = self.get_results(1, "POST", "", payload)
        nf_info = nf_info.json()
        result = nf_info['items'][0]
        del result['links']
        return result

    def find_ICMS(self, numero_nota: str):
        payload = {
            "q": f"SELECT custrecord_enl_taxamount FROM customrecord_enl_taxtrans WHERE custrecord_enl_tt_orderid='{numero_nota}' AND custrecord_enl_taxcode='icmsSt'"
        }
        icms_info = self.get_results(1, "POST", "", payload)
        result = icms_info.json()
        return result

    def get_UF(self, id_uf: str):
        url_ = f'https://7586908.suitetalk.api.netsuite.com/services/rest/record/v1/customer/{id_uf}/addressBook'
        temp_url, mun_, mun1, result = "", "", "", ""
        dados_uf = {}
        temp_response = requests.Response()
        temp_response.status_code = 400
        for i in range(0, 3):
            while temp_response.status_code != 200:
                temp_url = self.get_results(1, "GET", url_, "")
                try:
                    temp_response.status_code = temp_url.status_code
                except:
                    pass
            temp_response.status_code = 400
            if i == 0:
                temp_url = temp_url.json()
                url_ = temp_url['items'][0]['links'][0]['href']
            elif i == 1:
                temp_url = temp_url.json()
                url_ = temp_url['addressBookAddress']['links'][0]['href']
            else:
                dados_uf = temp_url.json()
                mun1 = dados_uf['custrecord_enl_city']['refName']
                break
        nome = cd.remove_capital_and_accents(mun1)
        uf_ = dados_uf['custrecord_enl_uf']['refName']
        uf1 = uf_.lower()
        for estado in cd.municipios_br:
            if uf1 in estado:
                for municipio in estado[uf1]:
                    if nome in municipio:
                        mun_: str = str(municipio[nome])[2:]
        result = mun_, uf_
        return result

    def check_gnre(self, id):
        payload = {"custbody_can_gerougnreemlote": True}
        url = f"https://7586908.suitetalk.api.netsuite.com/services/rest/record/v1/invoice/{id}"
        response = self.get_results(1, "PATCH", url, payload)
        return response
