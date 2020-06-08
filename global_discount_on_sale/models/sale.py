from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_discount = fields.Float('Discount(%)')
    discount_amount = fields.Monetary(
        string="Discount", compute="_amount_all")
    show_discount = fields.Boolean(
        string='Show Discount',
        default=lambda self: True if self.env.user.has_group(
            'global_discount_on_sale.is_global_discount') else False,
        compute='show_discount_field')

    def show_discount_field(self):
        if self.env.user.has_group(
                'global_discount_on_sale.is_global_discount') and \
                self.state in ['draft']:
            self.show_discount = True
        else:
            self.show_discount = False

    @api.depends('order_line.price_total', 'global_discount',
                 'discount_amount')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            discount = amount_untaxed * ((order.global_discount) / 100.0)
            amount_untaxed = amount_untaxed - discount
            order.update({
                'discount_amount': discount,
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax
            })

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_amount': self.discount_amount,
            'global_discount': self.global_discount,
        })
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id',
                 'order_id.global_discount')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit - line.price_unit * (
                1 - (line.discount or 0.0) / 100.0)
            total = line.price_unit * line.product_uom_qty - price
            discount = total * \
                ((line.order_id.global_discount) / 100.0)

            discount_amount_tax = total - discount
            taxes = line.tax_id.compute_all(discount_amount_tax,
                                            line.order_id.currency_id,
                                            line.product_uom_qty,
                                            product=line.product_id,
                                            partner=line.order_id.
                                            partner_shipping_id)
            line.update({
                'price_tax': sum(
                    t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': total,
            })
