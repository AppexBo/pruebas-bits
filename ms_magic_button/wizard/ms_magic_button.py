import time
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MsMagicButton(models.TransientModel):
    _name = "ms.magic.button"
    _description = "Magic Button"

    action = fields.Selection([
        ('remove_expired_notification', 'Remove Expired Notification')
    ], string="Action", default="remove_expired_notification")

    def action_magic(self):
        getattr(self, f'action_{self.action}')()

    def action_remove_expired_notification(self):
        query = f"""
            SELECT
                id
            FROM
                mail_activity
            WHERE
                date_deadline < '{fields.Date.to_string(fields.Date.today())}'
        """
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        for res in result:
            activity_id = self.env['mail.activity'].browse(res['id'])
            activity_id.unlink()
