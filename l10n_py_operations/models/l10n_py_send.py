# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import base64
import requests
from requests.auth import HTTPBasicAuth
import json

import logging
_logger = logging.getLogger(__name__)



class L10nPySend(models.Model):
    
    _inherit = ['account.move']
    
    def to_base64(self):
        if self.xml_str_format:
            text_bytes = str(self.xml_str_format).encode('utf-8')
            text_base64 = base64.b64encode(text_bytes)
            self.write(
                {
                    'format_base64_xml' : text_base64,
                    'py_file_content' : text_base64,
                }
            )
        else:
            raise UserError('No se genero una estructura XML')
        
    def get_header(self):
        sync_point_id = self.company_id.get_sync_point_id()  # SyncPointId proporcionado
        
        api_key = self.company_id.get_api_key()  # ApiKey proporcionado
        #ruc = "88888888"  # RUC de la empresa

        # Generar el valor de autenticación
        auth_value = f"{sync_point_id}:{api_key}" #:{ruc}"

        return {
            "Authorization": f"Basic {auth_value}",
            "Content-Type": "application/json"
        }

        
    def py_document_register(self):

        headers = self.get_header()


        endpoint =  self.env['l10n.py.endpoint'].search(
            [
                ('operation_type','=','send'),
                ('method','=','POST'),
                ('name','=','Envío de documentos' if self.company_id.use_endpoints_test else 'Envío de documentos (Produccion)' ),
                
            ]
        ) #"https://api-sandbox.hermesweb.net/api/Document/SendDocumentToAuthority"
        if endpoint:
            url = endpoint.url
            _logger.info('ENDPOINT')
            _logger.info(url)
            data = {
                "mapping": self.company_id.get_py_mapping(),
                "sign": "true" if self.company_id.to_sign else "false" ,
                "defaultCertificate": "true" if self.company_id.defaultCertificate else "false",
                "async": "true" if self.company_id.test_environment else 'false',
                "fileContent": self.format_base64_xml
            }

            _logger.info(f"DATA: {data}")

            try:
                response = requests.post(url, json=data, headers=headers)
                _logger.info(response.status_code)
                if response.status_code == 200:
                    response_json = response.json()
                    _logger.info(response_json)
                    self.write({'l10n_py_response' : response_json})
                    self.process_response(response_json)
                else:
                    _logger.info('Error en la autenticación o envío:')
                    _logger.info(response.status_code)
                    _logger.info(response.text)
                    raise UserError(f"Error al conectar con el servicio: {response.status_code}, {response.text}")
                    
            except requests.exceptions.RequestException as e:
                _logger.info("Error al conectar con el servicio:")
                _logger.info(e)
                raise UserError(f"Error al conectar con el servicio: {e}")
               
                


    def process_response(self, response : dict):
        
        try:
            response = json.loads(response)
            res_data = {}
            # res_data['l10n_py_response_Success'] = response.get('Success', False)

            # self.write(res_data)
            # 
            extra_info = ''
            for key, value in response.items():
                _field = f"l10n_py_response_{key}"
                _field_value = getattr(self,_field,None)
                if _field_value != None:
                    res_data[_field] = value or False
                else:
                    extra_info += f'No se encontro el campo: {_field} = {value} |'
            if res_data:
                self.write(res_data)
            if extra_info:
                self.write(
                    {
                        'l10n_py_response_extra_info' : extra_info,
                        'l10n_py_transaction' : not self.l10n_py_response_ErrorException,
                        'edi_py_state': 'sent' if self.l10n_py_response_Code == 0 else 'observed'
                    }
                )
            
                
        except Exception as e:
            _logger.info(f"Error al procesar respuesta: {e}")


    """
        {
            "":false,
            "":"00000000-0000-0000-0000-000000000000",
            "":"01801025443001001000000322024111218961756309",
            "":null,
            "Messages":null,
            "ResponseValue":"",
            "Extra":null,
            "":99,
            "":"Error de validación.",
            "ErrorException":"The 'http://ekuatia.set.gov.py/sifen/xsd:dBasGravIVA' element is invalid - The value '0.9090909090909091' is invalid according to its datatype 'http://ekuatia.set.gov.py/sifen/xsd:tMontoBase' - The FractionDigits constraint failed.",
            "Folio":0
        }
    """



    def action_py_request_document(self):
        pass

    def get_request_pdf(self):
        sync_point_id = self.company_id.get_sync_point_id()  # SyncPointId proporcionado
        
        api_key = self.company_id.get_api_key()  # ApiKey proporcionado
        #ruc = "88888888"  # RUC de la empresa

        # Generar el valor de autenticación
        auth_value = f"{sync_point_id}:{api_key}" #:{ruc}"

        header = {
            "Authorization": f"Basic {auth_value}",
            "Content-Type": "application/json"
        }

        endpoint =  self.env['l10n.py.endpoint'].search(
            [
                ('name','=','Descarga PDF' if self.company_id.use_endpoints_test else 'Descarga PDF (Produccion)'),
                ('method','=','GET')
            ]
        )
        if endpoint:
            URL = endpoint.url
            _logger.info('ENDPOINT')
            _logger.info(URL)
            
            URL += self.l10n_py_response_CountryDocumentId
            _logger.info(self.l10n_py_response_CountryDocumentId)

            try:
                response = requests.get(URL, headers=header, timeout=30)

                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    _logger.info('INFORMACION')
                    res : dict = response.json()
                    _logger.info(f"{res}")
                    documentBase64 = res.get('Base64Content', False)
                    return documentBase64
                else:
                    raise UserError(f"Error en la autenticación o consulta: {response.status_code}, {response.text}")
                    _logger.info(f"Error en la autenticación o consulta: {response.status_code}, {response.text}")
            except requests.exceptions.Timeout:
                _logger.error("El servicio PDF demoró demasiado en responder.")
                if self.l10n_py_response_extra_info:
                    self.write({'l10n_py_response_extra_info' : self.l10n_py_response_extra_info + '|El servicio PDF demoró demasiado en responder.'})
                else:
                    self.write({'l10n_py_response_extra_info' : '|El servicio PDF demoró demasiado en responder.'})

                return False
            except requests.exceptions.RequestException as e:
                raise UserError(f"Error al conectar con el servicio: {e}")
                _logger.info(f"Error al conectar con el servicio: {e}")
                

    def action_py_request_pdf(self):
        _name_file = f"{self.name}-{self.company_id.vat}-(PY)"
        attacht_id = self.env['ir.attachment'].search(
                [('res_model', '=', self._name), ('res_id', '=', self.id), ('name', '=', _name_file)], limit=1)

        if not attacht_id:        
            if self.l10n_py_response_CountryDocumentId:
                pdf = self.get_request_pdf()
                if pdf:
                    pdf = base64.b64decode(pdf)
                    self.env['ir.attachment'].create({
                            'res_model': self._name,
                            'res_id': self.id,
                            'type': 'binary',
                            'name': _name_file,
                            'datas': base64.b64encode(pdf),
                            'mimetype': 'application/pdf',
                        })
                    
            else:
                raise UserError('No se encontro el CDC para la factura')