from datetime import datetime

from netsuite_rest import gnre_methods
from . import xml_build


class Gerador:
    def __init__(self):
        self.obj_bd = gnre_methods.Gerador_Methods()
        self.obj_creator = xml_build.Create()

    def criar_unique(self, nf_number=None):
        agregado_xml = ""
        nf_encontrada = self.obj_bd.get_NFE_unique(nf_number)
        try:
            ns_id_1 = nf_encontrada.get('id_doc_fiscal')
            netsuite_id = nf_encontrada.get('ns_id')
            uf_e_mun = self.obj_bd.get_UF(netsuite_id)
            uf_ = uf_e_mun[1]
            mun = uf_e_mun[0]
            if not uf_ == 'SP':
                valor_nota = float(nf_encontrada.get('total_icmsts'))
                valor_nota = '{:.2f}'.format(valor_nota)
                ie = nf_encontrada.get('ie_cliente')
                cliente_nome = nf_encontrada.get('razao_social')
                chave_acesso = nf_encontrada.get('key_value')
                xml_buildado = self.obj_creator.create_gnre(uf_, ie, valor_nota, chave_acesso)
                agregado_xml += xml_buildado
                self.obj_bd.check_gnre(ns_id_1)
        except Exception as e:
            print(e)
        if agregado_xml != '':
            final = self.gerar_xml_final(agregado_xml)
            return final
        else:
            return "Inexistente"

    def criar_guias_em_lote(self, data_de_inicio: str, data_de_termino: str):
        agregado_xml = ""
        try:
            nfs_do_dia = self.obj_bd.get_NFE(data_de_inicio, data_de_termino)
            for nota in nfs_do_dia:
                try:
                    ns_id_1 = nota.get('id_doc_fiscal')
                    netsuite_id = nota.get('ns_id')
                    uf_e_mun = self.obj_bd.get_UF(netsuite_id)
                    uf_ = uf_e_mun[1]
                    mun = uf_e_mun[0]
                    checked = nota.get('flag')
                    if not uf_ == 'SP' and checked != 'T':
                        valor_nota = nota.get('total_icmsts')
                        valor_nota = '{:.2f}'.format(valor_nota)
                        ie = nota.get('ie_cliente')
                        cliente_nome = nota.get('razao_social')
                        chave_acesso = nota.get('key_value')
                        xml_buildado = self.obj_creator.create_gnre(uf_, ie, valor_nota, chave_acesso)
                        agregado_xml += xml_buildado
                        self.obj_bd.check_gnre(ns_id_1)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            return False
        if agregado_xml != '':
            final = self.gerar_xml_final(agregado_xml)
            return final
        else:
            return "Inexistente"

    def get_time(self):
        agora = datetime.now()
        return agora.strftime("%Y-%m-%d_%H:%M:%S")

    def gerar_xml_final(self, xml_agregado):
        try:
            string_format = ""
            for item in xml_agregado:
                string_format += item
            xml_final = self.obj_creator.create_xml(string_format)
            return xml_final
        except Exception as e:
            print(e)
            return False
