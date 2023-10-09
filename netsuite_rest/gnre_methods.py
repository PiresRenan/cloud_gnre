import json

import requests

from gerador_de_lotes_gnre import cd
from .connection import NS_Services


class Gerador_Methods(NS_Services):

    def get_NFE(self, data_comeco: str, data_limite: str):
        result = []
        payload = {
            "q": f"SELECT "
                 f"t.id AS id_doc_fiscal, "
                 f"t.custbody_acs_candide_responsavel_ls AS resp, "
                 f"t.custbodycan_stliberada AS st_liberada, "
                 f"t.createdby AS criado_apartir_de, "
                 f"t.custbody_avlr_document_code AS nf_avalara_code, "
                 f"t.custbody_enl_linknotafiscal AS url_nf, "
                 f"t.trandate AS data_da_nota, "
                 f"t.custbody_enl_fiscaldocnumber AS n_nf, "
                 f"t.custbody_can_gerougnreemlote AS flag, "
                 f"t.custbody_enl_accesskey AS key_value, "
                 f"t.custbody_enl_linknotafiscal AS url, "
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
                 f"t.trandate >= '{ data_comeco }' AND t.trandate <= '{ data_limite }' AND "
                 f"t.type = 'CustInvc' AND t.approvalstatus = '2' AND t.custbodycan_stliberada = 'T' AND "
                 f"tx_trans.custrecord_enl_taxcode = 'icmsSt' AND t.custbody_can_gerougnreemlote = 'F' AND "
                 f"c.custentitycan_ufcli_paragnre!='SP' AND c.custentitycan_ufcli_paragnre!='RJ' "
                 f"GROUP BY "
                 f"t.id, t.createdby, t.custbodycan_stliberada, t.custbody_avlr_document_code, t.custbody_enl_linknotafiscal, t.custbody_enl_fiscaldocnumber, "
                 f"t.trandate, t.custbody_can_gerougnreemlote, t.custbody_enl_accesskey, t.custbody_acs_candide_responsavel_ls, c.custentity_enl_cnpjcpf, "
                 f"c.companyname, c.id, c.custentity_enl_legalname, c.custentity_enl_ienum, c.custentitycan_ufcli_paragnre, t.custbody_enl_linknotafiscal"
        }
        nf_info = self.get_results(1, "POST", "", payload)
        nf_info = nf_info.json()
        for nf in nf_info['items']:
            del nf['links']
            result.append(nf)
        return result

    def get_NFE_unique(self, nf_number=None):
        nf_number = str(nf_number)
        if len(nf_number) < 9:
            nf_number = nf_number.zfill(9)
        result = []
        payload = {
            "q": "SELECT t.custbody_acs_candide_responsavel_ls AS resp, t.custbodycan_stliberada AS st_liberada, t.id AS id_doc_fiscal, "
                 "t.createdby AS criado_apartir_de, t.custbody_avlr_document_code AS nf_avalara_code, t.custbody_enl_linknotafiscal AS url_nf, "
                 "t.trandate AS data_da_nota, t.custbody_enl_fiscaldocnumber AS n_nf, t.custbody_can_gerougnreemlote AS flag, t.custbody_enl_accesskey AS key_value, "
                 "c.custentity_enl_cnpjcpf AS cnpj, c.companyname AS cliente, c.id AS ns_id, c.custentity_enl_legalname AS razao_social, "
                 "c.custentity_enl_ienum AS ie_cliente, c.custentitycan_ufcli_paragnre AS uf, SUM(tx_trans.custrecord_enl_taxamount) AS total_ICMSTS "
                 "FROM "
                 "transaction AS t LEFT JOIN customer AS c ON c.id=t.entity LEFT JOIN customrecord_enl_taxtrans AS tx_trans ON tx_trans.custrecord_enl_tt_orderid=t.id "
                 "WHERE "
                 "t.custbody_enl_fiscaldocnumber = '{}' AND "
                 "t.type = 'CustInvc' AND t.approvalstatus = '2' AND "
                 "tx_trans.custrecord_enl_taxcode = 'icmsSt' AND "
                 "c.custentitycan_ufcli_paragnre != 'SP' AND c.custentitycan_ufcli_paragnre != 'RJ' "
                 "GROUP BY "
                 "t.id, t.createdby, t.custbody_avlr_document_code, t.custbody_enl_linknotafiscal, t.custbody_enl_fiscaldocnumber, t.trandate, t.custbodycan_stliberada, "
                 "t.custbody_can_gerougnreemlote, t.custbody_enl_accesskey, c.custentity_enl_cnpjcpf, c.companyname, c.id, c.custentity_enl_legalname, c.custentity_enl_ienum, "
                 "c.custentitycan_ufcli_paragnre, t.custbody_acs_candide_responsavel_ls".format(nf_number)
        }
        nf_info = self.get_results(1, "POST", "", payload)
        nf_info = nf_info.json()
        result = nf_info['items'][0]
        del result['links']
        return result

    def check_gnre(self, id):
        payload = {"custbody_can_gerougnreemlote": True, "custbodycan_stliberada": True}
        url = f"https://7586908.suitetalk.api.netsuite.com/services/rest/record/v1/invoice/{id}"
        response = self.get_results(1, "PATCH", url, payload)
        return response
