# -*- coding:utf-8 -*-

from odoo import api, models, fields
import base64
import io
import logging
_logger = logging.getLogger(__name__)



class AccountMoveSend(models.TransientModel):
    _inherit = ['account.move.send']   

    
    
    @api.model
    def _prepare_invoice_pdf_report(self, invoice, invoice_data):
        if invoice.invoice_pdf_report_id:
            return

       
        if invoice[0].company_id.use_auto_invoice:
            content, _report_format = self.env['ir.actions.report']._render(
                 'l10n_py_operations.ir_actions_report_invoice_py_1', invoice.ids
             )
            invoice_data['pdf_attachment_values'] = {
                'raw': content,
                'name': invoice._get_invoice_report_filename(),
                'mimetype': 'application/pdf',
                'res_model': invoice._name,
                'res_id': invoice.id,
                'res_field': 'invoice_pdf_report_file',  # Binary field
            }
        else:
            content = invoice.get_request_pdf()
            if content:
                pdf_binary_content = base64.b64decode(content)
                # Usamos io.BytesIO en lugar de escribir en disco, esto dado que tenemos un error de escritura en el contenedor
                # Siempre usar io.BytesIO para generar pdf!
                pdf_buffer = io.BytesIO(pdf_binary_content)

                invoice_data['pdf_attachment_values'] = {
                    'raw': pdf_buffer.getvalue(),
                    'name': invoice._get_invoice_report_filename(),
                    'mimetype': 'application/pdf',
                    'res_model': invoice._name,
                    'res_id': invoice.id,
                    'res_field': 'invoice_pdf_report_file',
                }
            else:
                super(AccountMoveSend, self)._prepare_invoice_pdf_report(invoice, invoice_data)