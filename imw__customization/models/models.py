# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import api, fields, models, _
 

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    imw_qty = fields.Float(string='Quantity')
    imw_measurement = fields.Float(string='Measurement',default=1)
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')
 
 
class imw_product_template(models.Model):
    #_name = 'product.template'
    _inherit = 'product.template'
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')
