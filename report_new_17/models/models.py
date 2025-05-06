from odoo import api, models, fields
from odoo.exceptions import UserError
import json
import logging
from num2words import num2words

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_bo_exchange_rate = fields.Float('Tipo de cambio', store=True, compute='_compute_l10n_bo_exchange_rate')

    @api.depends('currency_id')
    def _compute_l10n_bo_exchange_rate(self):
        for move in self:
            if move.currency_id.rate > 0:
                move.l10n_bo_exchange_rate = 1 / move.currency_id.rate
            else:
                move.l10n_bo_exchange_rate = 1.00

    def number_to_word(self, number: float):
        decimal_part = int(round(number % 1, 2) * 100)
        integer_part = int(number)
        # get actual language
        lang = self.env.context.get('lang', 'es_ES')
        return f"{num2words(integer_part, lang=lang)} con {decimal_part}/100 {self.currency_id.symbol}"

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Factura - %s' % (self.name)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
