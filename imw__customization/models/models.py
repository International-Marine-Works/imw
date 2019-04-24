# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import api, fields, models

class imw_product_template(models.Model):
    #_name = 'product.template'
    _inherit = 'product.template'
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')
