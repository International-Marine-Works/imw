# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import api, fields, models

 
class imw_product_template(models.Model):
    #_name = 'product.template'
    _inherit = 'product.template'
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    imw_qty = fields.Float(string='Quantity')
    imw_measurement = fields.Float(string='Measurement',default=1)
    category_id = fields.Many2one('product.category', 'category')
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')

    @api.multi
    @api.onchange('imw_qty')
    def _value_pc(self):
        self.product_qty = float(self.imw_qty) * float(self.imw_measurement)

