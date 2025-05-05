# -*- coding:utf-8 -*-

from odoo import api, models, fields
from datetime import datetime
import pytz
from lxml import etree

from odoo.exceptions import ValidationError, UserError
import base64

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = ['account.move']    

    
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------------------------
    

    def compate_t_name(self):
        return

    def validate_xml(self, xml_str, xsd_path):
        if xml_str and xsd_path:
            try:
                with open(xsd_path, 'rb') as xsd_file:
                    xmlschema_doc = etree.parse(xsd_file)
                    xmlschema = etree.XMLSchema(xmlschema_doc)
                    
                parser = etree.XMLParser(recover=True)
                xml_doc = etree.fromstring(xml_str.encode('utf-8'), parser)

                if not xmlschema.validate(xml_doc):
                    # Obtener los errores de validación
                    log = xmlschema.error_log
                    error_details = "\n".join([f"Linea {error.line}: {error.message}" for error in log])
                    raise ValidationError(f"El XML no es válido según el esquema XSD proporcionado.\nErrores:\n{error_details}")
            except (etree.XMLSyntaxError, etree.XMLSchemaParseError) as e:
                raise ValidationError(f"Error al analizar el XML o el esquema XSD: {str(e)}")
            except IOError as e:
                raise ValidationError(f"No se pudo leer el archivo XSD: {str(e)}")
            


    def _post(self, soft=True):
        res : models.Model =  super(AccountMove, self)._post(soft)
        for record in res:
            if record.move_type == 'out_invoice' and record.journal_id.sudo().l10n_latam_use_documents:
                record.prepare_py_invoice()
                if record.l10n_py_response_Code != 0:
                    raise UserError(record.l10n_py_response_ErrorException)
        return res
    
    def prepare_py_invoice(self):
        if self.move_type == 'out_invoice':
            self.prepare_out_invoice()

    
    def prepare_out_invoice(self):
        if self.l10n_latam_document_type_id:
            if self.l10n_latam_document_type_id and self.l10n_latam_document_type_id.internal_type == 'invoice':
                xml_str = self.generate_str_xml_1()
                _logger.info(xml_str)
                self.write({'xml_str_format' : xml_str})
                self.to_base64()
                self.py_document_register()





    def generate_str_xml_1(self):
        str_format = '<rDE xmlns="http://ekuatia.set.gov.py/sifen/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance siRecepDE_v150.xsd">'
        
        AA002 = self.get_AA002()
        str_format += f'<dVerFor>{AA002}</dVerFor>'
        
        str_format += '<DE>'
        A003 = self.get_A003()
        str_format += f'<dDVId>{A003}</dDVId>'
        
        A004 = self.get_A004()
        str_format += f'<dFecFirma>{A004}</dFecFirma>'

        A005 = self.get_A005()
        str_format += f'<dSisFact>{A005}</dSisFact>'
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        str_format += self.get_group_B()
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        str_format += self.get_group_C()
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        str_format += self.get_group_D()
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        str_format += self.get_group_E()
        #---------------------------------------------------------------
        str_format += self.get_group_F()
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        
        str_format += '</DE>'
        str_format += '</rDE>'
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        
        return str_format
    

    

    def get_group_B(self):
        str_format = '<gOpeDE>'
        
        B002, B003 = self.get_B002(), self.get_B003()
        
        str_format += f'<iTipEmi>{B002}</iTipEmi>'
        str_format += f'<dDesTipEmi>{B003}</dDesTipEmi>'
        
        B004 = self.get_B004(nit=self.getRUC(),numero_factura=int(self.get_invoice_number()),punto_venta=self.get_C006())
        str_format += f'<dCodSeg>{B004}</dCodSeg>'

        B005 = self.get_B005()
        str_format += f'<dInfoEmi>{B005}</dInfoEmi>'

        B006 = self.get_B006()
        str_format += f'<dInfoFisc>{B006}</dInfoFisc>'
        
        str_format += '</gOpeDE>'
        return str_format
    
    def get_group_C(self) -> str:
        "XML C. Campos de datos del Timbrado (C001-C099)"

        str_format = '<gTimb>'
        
        C002, C003 = self.get_C002(), self.get_C003()

        str_format += f'<iTiDE>{C002}</iTiDE>'
        str_format += f'<dDesTiDE>{C003}</dDesTiDE>'
        
        C004 = self.get_C004()
        
        str_format += f'<dNumTim>{C004}</dNumTim>' 

        C005, C006 = self.get_C005(), self.get_C006()
        
        str_format += f'<dEst>{C005}</dEst>'        
        str_format += f'<dPunExp>{C006}</dPunExp>'     

        C007 = self.get_invoice_number(ir_next = True)
        str_format += f'<dNumDoc>{C007}</dNumDoc>'
        
        C010 = self.get_serial_number()
        if C010:
            str_format += f'<dSerieNum>{C010}</dSerieNum>'

        C008 = self.get_C008()
        C009 = self.get_C009()
        
        str_format += f'<dFeIniT>{C008}</dFeIniT>'
        #str_format += f'<dFeFinT>{C009}</dFeFinT>'
        
        str_format += '</gTimb>'
        return str_format
    
    def get_group_D(self) -> str:
        "XML D. Campos Generales del Documento Electrónico DE (D001-D299)"
        #---------------------------------------------------------------
        str_format = '<gDatGralOpe>'
        str_format += f'<dFeEmiDE>{self.get_emision_date()}</dFeEmiDE>'
        #---------------------------------------------------------------
        
        str_format += self.get_group_D1()
        #---------------------------------------------------------------
        str_format += self.get_group_D2()
        #---------------------------------------------------------------
        str_format += self.get_group_D3()
        #---------------------------------------------------------------
        
        str_format += '</gDatGralOpe>'
        return str_format

    def get_group_D1(self) -> str:
        "Campos inherentes a la operación comercial (D010-D099)"
        if self.get_C002() != '7':
            D010 = '<gOpeCom>'

            D011 = self.get_D011()
            D010 += f'<iTipTra>{D011}</iTipTra>'
            
            D012 = self.get_D012()
            D010 += f'<dDesTipTra>{D012}</dDesTipTra>'
            
            D013 = self.get_D013()
            
            D010 += f'<iTImp>{D013}</iTImp>'
            
            D014 = self.get_D014()
            D010 += f'<dDesTImp>{D014}</dDesTImp>'
            
            D015, D016 = self.get_D015(), self.get_D016()
            
            D010 += f'<cMoneOpe>{D015}</cMoneOpe>'
            D010 += f'<dDesMoneOpe>{D016}</dDesMoneOpe>'
            D010 += '</gOpeCom>'
            
            return D010
        return ''
    
    def get_group_D2(self):
        str_format = '<gEmis>'
        D101, D102 = self.getRUC(), self.getDigitVerRUC()
        D103, D104 = self.get_taxpayer_type(), ''
        D105, D106 = self.get_name_reazon_social(), ''
        D107, D108 = self.get_address(), self.get_number_house()

        str_format += f'<dRucEm>{D101}</dRucEm>'
        str_format += f'<dDVEmi>{D102}</dDVEmi>'
        str_format += f'<iTipCont>{D103}</iTipCont>'
        str_format += f'<dNomEmi>{D105}</dNomEmi>'
        str_format += f'<dDirEmi>{D107}</dDirEmi>'
        str_format += f'<dNumCas>{D108}</dNumCas>'
        
        
        D111, D112 = self.get_department_info()
        D113, D114 = self.get_department_distrit_info()
        D115, D116 = self.get_department_distrit_city_info()
        D117 = self.get_document_issuer_phone_number()
        D118 = self.get_emisor_email()

        str_format += f'<cDepEmi>{D111}</cDepEmi>'
        str_format += f'<dDesDepEmi>{D112}</dDesDepEmi>'
        str_format += f'<cDisEmi>{D113}</cDisEmi>'
        str_format += f'<dDesDisEmi>{D114}</dDesDisEmi>'
        str_format += f'<cCiuEmi>{D115}</cCiuEmi>'
        str_format += f'<dDesCiuEmi>{D116}</dDesCiuEmi>'
        str_format += f'<dTelEmi>{D117}</dTelEmi>'
        str_format += f'<dEmailE>{D118}</dEmailE>'

        str_format += self.get_group_D2_1()
        str_format += self.get_group_D2_2()
        
        str_format += '</gEmis>'
        return str_format

    def get_group_D2_1(self):
        AcEco, DesAcEco = self.get_econonic_activity_id_info()
        str_format = '<gActEco>'
        str_format += f'<cActEco>{AcEco}</cActEco>'
        str_format += f'<dDesActEco>{DesAcEco}</dDesActEco>'
        str_format += '</gActEco>'
        return str_format
    
    def get_group_D2_2(self):
        return ''
    
    def get_group_D3(self):
        D201, D202 = self.get_receiver_nature(), self.get_receiver_operation()
        D203, D204 = self.get_receiver_country_info()
        
        str_format = '<gDatRec>'
        str_format += f'<iNatRec>{D201}</iNatRec>'
        str_format += f'<iTiOpe>{D202}</iTiOpe>'
        str_format += f'<cPaisRec>{D203}</cPaisRec>'
        str_format += f'<dDesPaisRe>{D204}</dDesPaisRe>'

        D205 = ''
        D206 = ''
        D207 = ''
        if D201 == '1':
            D205 = self.get_receiver_taxpayer_type()
            str_format += f'<iTiContRec>{D205}</iTiContRec>'

            D206 = self.get_receiver_ruc()
            str_format += f'<dRucRec>{D206}</dRucRec>'
            
            if D206:
                D207 = self.get_receiver_digit_ver()
                str_format += f'<dDVRec>{D207}</dDVRec>'
        
        D208 = ''
        if D201 == '2' and D202 != '4':
            D208 = self.get_D208()
            str_format += f'<iTipIDRec>{D208}</iTipIDRec>'
        
        D209 = ''
        if D208:
            # Revisar posteriormente el tipo de documentos = 9 OTROS
            D209 = self.get_D209()
            str_format += f'<dDTipIDRec>{D209}</dDTipIDRec>'

        
        D210 = ''
        if D201 == '2' and D202 != '4':
            if D208 == '5':
                D210 = '0'
            else:
                D210 = self.get_D210()
            str_format += f'<dNumIDRec>{D210}</dNumIDRec>'

        D211 = self.get_receiver_name() if D208 != '5' else 'Sin Nombre'
        str_format += f'<dNomRec>{D211}</dNomRec>'

        D212 = ''
        D213 = ''
        D218 = ''
        if D202 == '4' or self.get_C002() == '4':
            D213 = self.get_D213(self)
            str_format += f'<dDirRec>{D213}</dDirRec>'

            if D213:
                D218 = self.get_D218()
                str_format += f'<dNumCasRec>{D218}</dNumCasRec>'

        D219, D220 = '', ''
        if D213 and D202 != '4':
            D219, D220 = self.get_receiver_department_info()
            str_format += f'<cDepRec>{D219}</cDepRec>'
            str_format += f'<dDesDepRec>{D220}</dDesDepRec>'

        D221, D222 = self.get_receiver_department_distrit_info()
        if D221 and D222:
            str_format += f'<cDisRec>{D221}</cDisRec>'
            str_format += f'<dDesDisRec>{D222}</dDesDisRec>'
            
        D223, D224 = '', ''
        if D213 and D202 != '4':
            D223, D224 = self.get_receiver_department_distrit_city_info()
            str_format += f'<cCiuRec>{D223}</cCiuRec>'
            str_format += f'<dDesCiuRec>{D224}</dDesCiuRec>'

        D214 = '' # ..., D217 = ''
            
        str_format += '</gDatRec>'
        return str_format
    
    
    def get_group_E(self):
        str_format = '<gDtipDE>'
        if self.get_C002() == '1':
            str_format += self.get_group_E_1()

        if self.get_C002() in ['1','4']:
            str_format += self.get_group_E_7()

        str_format += self.get_group_E_8()
        str_format += '</gDtipDE>'
        return str_format
    
    def get_group_E_1(self):
        str_format = '<gCamFE>'

        E011 = self.get_E011()
        str_format += f'<iIndPres>{E011}</iIndPres>'
        
        E012 = self.get_E012()
        str_format += f'<dDesIndPres>{E012}</dDesIndPres>'
        
        E013 = ''
        str_format += '</gCamFE>'
        return str_format
    
    def get_group_E_7(self):
        str_format = '<gCamCond>'

        E601 = self.get_E601()
        str_format += f'<iCondOpe>{E601}</iCondOpe>'

        E602 = self.get_E602()
        str_format += f'<dDCondOpe>{E602}</dDCondOpe>'
        
        if E601 == '1':
            str_format += self.get_group_E_7_1()
        str_format += '</gCamCond>'
        return str_format
    
    def get_group_E_7_1(self):
        str_format = ''

        for line in self.l10n_py_payments_ids:
            
            str_format += '<gPaConEIni>'

            E606 = line.get_E606()
            str_format += f'<iTiPago>{E606}</iTiPago>'

            E607 = line.get_E607()
            str_format += f'<dDesTiPag>{E607}</dDesTiPag>'
            
            E608 = line.get_E608()
            str_format += f'<dMonTiPag>{E608}</dMonTiPag>'
            
            E609 = line.get_E609()
            str_format += f'<cMoneTiPag>{E609}</cMoneTiPag>'
            
            E610 = line.get_E610()
            str_format += f'<dDMoneTiPag>{E610}</dDMoneTiPag>'

            E611 = '' 
            if E609 != 'PYG':
                E611 = line.get_E611()
                str_format += f'<dTiCamTiPag>{E611}</dTiCamTiPag>'
            
            # E7.1.1
            if E606 in ['3','4']:
                str_format += line.get_group_7_1_1()


            str_format += '</gPaConEIni>'
        
        if not str_format:
            raise UserError("Esteblezca linea de metodos de pago (PY)")
        return str_format
    
    def get_invoice_items(self):
        return self.invoice_line_ids.filtered( lambda line: line.display_type == 'product' and line.product_id )
    
    def get_group_E_8(self):
        str_format = ''
        _C002 = self.get_C002()
        _D013 = self.get_D013()
        for line in self.get_invoice_items():    
                str_format += '<gCamItem>'
                
                E701 = line.get_E701()
                str_format += f'<dCodInt>{E701}</dCodInt>'
                
                E708 = line.get_E708()
                str_format += f'<dDesProSer>{E708}</dDesProSer>'
                
                E709 = line.get_E709()
                str_format += f'<cUniMed>{E709}</cUniMed>'
                
                E710 = line.get_E710()
                str_format += f'<dDesUniMed>{E710}</dDesUniMed>'
                
                E711 = line.get_E711()
                str_format += f'<dCantProSer>{E711}</dCantProSer>'
                
                if _C002 != '7':
                    str_format += line.get_group_E_8_1()
                
                if _D013 in ['1','3','4','5'] and _C002 not in ['4','7']:
                    str_format += line.get_group_E_8_2()
                    
                str_format += '</gCamItem>'
                
        return str_format
    
    def get_group_F(self):
        str_format = '<gTotSub>'
        
        F005 = self.get_F005()
        str_format += f'<dSub10>{F005}</dSub10>'

        F008 = self.get_F008()
        str_format += f'<dTotOpe>{F008}</dTotOpe>'
        
        F009 = self.get_F009()
        str_format += f'<dTotDesc>{F009}</dTotDesc>'
        
        F033 = self.get_F033()
        str_format += f'<dTotDescGlotem>{F033}</dTotDescGlotem>'
        
        
        F034 = self.get_F034()
        str_format += f'<dTotAntItem>{F034}</dTotAntItem>'
        
        F035 = self.get_F035()
        str_format += f'<dTotAnt>{F035}</dTotAnt>'
        
        F010 = self.get_F010()
        str_format += f'<dPorcDescTotal>{F010}</dPorcDescTotal>'
        
        F011 = self.get_F011()
        str_format += f'<dDescTotal>{F011}</dDescTotal>'
        
        # F011 = self.get_F011()
        # str_format += f'<dDescTotal>{F011}</dDescTotal>'

        F012 = self.get_F012()
        str_format += f'<dAnticipo>{F012}</dAnticipo>'

        F013 = self.get_F013()
        str_format += f'<dRedon>{F013}</dRedon>'


        F014 = self.get_F014()
        str_format += f'<dTotGralOpe>{F014}</dTotGralOpe>'
        
        F016 = self.get_F016()
        str_format += f'<dIVA10>{F016}</dIVA10>'
        
        F017 = self.get_F017()
        str_format += f'<dTotIVA>{F017}</dTotIVA>'
        
        F019 = self.get_F019()
        str_format += f'<dBaseGrav10>{F019}</dBaseGrav10>'

        
        F020 = self.get_F020()
        str_format += f'<dTBasGraIVA>{F020}</dTBasGraIVA>'
        
        F023 = 0
        if self.get_D015() != 'PYG':
            F023 = self.get_F023()
            str_format += f'<dTotalGs>{F023}</dTotalGs>'
            
        
        

        str_format += '</gTotSub>'
        return str_format
        
    


    
    # @api.depends('name')
    # def _compute_l10n_latam_document_number(self):
    #     l10n_py_document = True
    #     recs_with_name = self.filtered(lambda x: x.name != '/')
    #     for rec in recs_with_name:
    #         if rec.l10n_latam_document_type_id and rec.establishment_id and rec.expedition_point_id:
                
    #             name = rec.name
    #             doc_code_prefix = rec.l10n_latam_document_type_id.doc_code_prefix
    #             if doc_code_prefix and name and rec.establishment_id and rec.expedition_point_id and not rec.l10n_latam_document_number:
    #                 name = rec.get_invoice_number() #name.split(" ", 1)[-1]
    #                 name = f"{rec.establishment_id.get_code()} {rec.expedition_point_id.get_code()} {rec.get_serial_number()} {name}"
    #             elif doc_code_prefix and rec.l10n_latam_document_number:
    #                 name = rec.l10n_latam_document_number

    #         else:
    #             l10n_py_document = False
    #             break

    #         if l10n_py_document:
    #             rec.l10n_latam_document_number = name
    #     if l10n_py_document:
    #         remaining = self - recs_with_name
    #         remaining.l10n_latam_document_number = False
    #     else:
    #         super(AccountMove, self)._compute_l10n_latam_document_number()
            

    @api.depends('posted_before', 'state', 'journal_id', 'date', 'move_type', 'payment_id')
    def _compute_name(self):
        self = self.sorted(lambda m: (m.date, m.ref or '', m._origin.id))

        for move in self:
            if move.state == 'cancel':
                continue

            move_has_name = move.name and move.name != '/'
            if move_has_name or move.state != 'posted':
                if not move.posted_before and not move._sequence_matches_date():
                    if move._get_last_sequence():
                        # The name does not match the date and the move is not the first in the period:
                        # Reset to draft
                        move.name = False
                        continue
                else:
                    if move_has_name and move.posted_before or not move_has_name and move._get_last_sequence():
                        # The move either
                        # - has a name and was posted before, or
                        # - doesn't have a name, but is not the first in the period
                        # so we don't recompute the name
                        continue
            if move.l10n_latam_document_type_id and move.establishment_id and move.expedition_point_id and not move.l10n_latam_document_number:
                move.name = f"{move.l10n_latam_document_type_id.doc_code_prefix} {move.establishment_id.get_code()} {move.expedition_point_id.get_code()} {move.get_serial_number()} {move.get_invoice_number()}"
            elif move.l10n_latam_document_number and move.l10n_latam_document_type_id:
                move.name = f"{move.l10n_latam_document_type_id.doc_code_prefix} {move.l10n_latam_document_number}"
            else:
                super(AccountMove, self)._compute_name()
                break


    def button_cancel(self):
        super(AccountMove, self).button_cancel()
        self.write({'edi_py_state' : 'canceled'})


    def button_draft(self):
        super(AccountMove, self).button_draft()
        self.write({'edi_py_state' : 'pending'})