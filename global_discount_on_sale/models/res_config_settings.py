from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_id = fields.Many2one('account.account', string='Discount Account',
                                 store=True)

    @api.model
    def get_values(self):
        return {
            'account_id': self.env['ir.default'].sudo().get(
                'res.config.settings', 'account_id'),
        }

    @api.multi
    def set_values(self):
        IrValues = self.env['ir.default']
        IrValues.set('res.config.settings', 'account_id',
                     self.account_id.id)
