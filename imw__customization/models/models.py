# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_utils

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    imw_qty = fields.Float(string='Quantity')
    imw_measurement = fields.Float(string='Measurement',default=1)
    category_id = fields.Many2one('product.category', 'category')
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')

    @api.multi
    @api.onchange('imw_qty')
    def _value_pc(self):
        self.product_uom_qty = float(self.imw_qty) * float(self.imw_measurement)

    @api.multi
    @api.onchange('product_id', 'location_id')
    def product_filter(self):
        res = {}
        if self.product_id:
            res['domain'] = {'location_id': [('product_id', '=', self.product_id.id)]}
        return res



    @api.onchange('product_id')
    def onchange_product(self):
        res = {}
        # If no UoM or incorrect UoM put default one from product
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id
            res['domain'] = {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        return res



class imw_product_template(models.Model):
    #_name = 'product.template'
    _inherit = 'product.template'
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')





