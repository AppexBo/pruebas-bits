import io
import pytz
import logging
import base64

from odoo import fields, api, models
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

_logger = logging.getLogger(__name__)

class ReportMovementHistory(models.Model):
    _name = "report.movement.history"
    _description = "Report Movement History"


    def _default_start_date(self):
        return fields.Datetime.now() - timedelta(days=1)

    start_date = fields.Datetime(string="Fecha de Inicio", required=True, 
                                default=_default_start_date,
                                help="Fecha inicial del rango.")
    end_date = fields.Datetime(string="Fecha Final", required=True, 
                                default=fields.Datetime.now,
                                help="Fecha final del rango.")
    location_id = fields.Many2one('stock.location', string="Localización", required=True,
                                help="Elegir la localización.")
    product_ids = fields.Many2many( 'product.product', string='Productos', required=True, 
                                help="Elegir el producto."
    )

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def action_print_pdf(self):
        if self.start_date > self.end_date:
            raise ValidationError('La fecha de inicio debe ser menor que la fecha de finalización')
        
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'location': self.location_id.id,
            'product_ids': self.product_ids.mapped('id'),
        }

        data.update(
            self.get_sale_details(
                    data['start_date'], 
                    data['end_date'], 
                    data['location'], 
                    data['product_ids']
            )
        )

        data =  {
            'type': 'ir.actions.report',
            'report_name': 'report_movement_history.report_moves_history',  # Reemplaza con el nombre de tu reporte
            'report_type': 'qweb-pdf',
            'data': {
                'form': data,  # Aquí está tu diccionario con los datos
            }, 
            'context': self.env.context,
        }
        
        return data

    @api.model
    def get_sale_details(self, start_date=False, end_date=False, location=False, products=False):
        aux_start_date = start_date
        aux_end_date = end_date

        if aux_start_date:
            aux_start_date = fields.Datetime.from_string(aux_start_date)
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            aux_start_date = today.astimezone(pytz.timezone('UTC'))

        if aux_end_date:
            aux_end_date = fields.Datetime.from_string(aux_end_date)
            # avoid a aux_end_date smaller than aux_start_date
            if (aux_end_date < aux_start_date):
                aux_end_date = aux_start_date + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            aux_end_date = aux_start_date + timedelta(days=1, seconds=-1)

        domain = [
            '&', '&', 
            ('state', '=', 'done'),
            ('product_id', 'in', products),
            ('date', '<=', fields.Datetime.to_string(aux_end_date)),
            '|',
            ('location_id', '=', location),
            ('location_dest_id', '=', location),
        ]

        all_moves = self.env['stock.move.line'].search(domain, order='date')
        prods = self.env['product.product'].search([('id', 'in', products)])

        return{
            #'products': prods,
            'data': list(self._process_moves(products, all_moves, aux_start_date, location))
        }
        
    @api.model
    def _process_moves(self, products, all_moves, date_start, location):
        for product in products:
            lst = []
            total_out = 0
            total_in = 0
            opening_balance = 0
            balance = 0
            moves = all_moves.filtered(lambda r: r.product_id.id==product)

            if moves:
                # Cálculo del balance inicial (antes de date_start)
                balance = round(sum(
                    -line.quantity if line.location_id.id == location else line.quantity
                    for line in moves
                    if line.date <= date_start
                ), 2)
                opening_balance = balance
                moves = moves.filtered(lambda r: r.date >= date_start)

                for line in moves:
                    temp_dict = {}
                    
                    if location == line.location_id.id:
                        # Es una SALIDA (el producto sale de esta ubicación)
                        temp_dict['out'] = line.quantity
                        temp_dict['in'] = '--'
                        balance -= line.quantity  # Restar del balance
                        total_out += line.quantity
                    else:
                        # Es una ENTRADA (el producto entra a esta ubicación)
                        temp_dict['in'] = line.quantity
                        temp_dict['out'] = '--'
                        balance += line.quantity  # Sumar al balance
                        total_in += line.quantity
                    
                    # Agregar información adicional
                    temp_dict['date'] = line.date
                    temp_dict['picking_type'] = self.substitute(line.picking_code or '')  # Usar picking_code en lugar de picking_type_id.code
                    temp_dict['balance'] = balance
                    temp_dict['reference'] = line.reference or line.move_id.reference or line.picking_id.name or ''
                    
                    lst.append(temp_dict)

            yield {
                'opening_balance': opening_balance,
                'balance': balance,
                'total_in': total_in,
                'total_out': total_out,
                'lst': lst,
                'product_data': product,
            }

    @staticmethod
    def substitute(code):
        return code.replace('_', " ").title() if code else code


        
        
        


    def action_print_xlsx(self):
        # Crear un archivo CSV vacío con solo los encabezados
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados (puedes personalizarlos)
        writer.writerow(["Columna1", "Columna2", "Columna3"])  # Columnas vacías
        
        # Preparar el archivo para descarga
        file_data = base64.b64encode(output.getvalue().encode('utf-8'))
        
        # Actualizar el registro con el archivo generado
        self.write({
            'data_file': file_data,
            'file_name': 'reporte.csv'
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=report.movement.history&id={}&field=data_file&filename_field=file_name&download=true'.format(self.id),
            'target': 'self',
        }

    #def action_get_xlsx_report(self, data, response):
    