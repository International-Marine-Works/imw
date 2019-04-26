# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
 
#class PurchaseOrderLine(models.Model):
    #   _inherit = 'purchase.order.line'

    #    imw_qty = fields.Float(string='Quantity')
    #   imw_measurement = fields.Float(string='Measurement',default=1)
    #   category_id = fields.Many2one('product.category', 'category')
    #  otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')

    #   @api.multi
    #  @api.onchange('imw_qty')
    #  def _value_pc(self):
    #      self.product_qty = float(self.imw_qty) * float(self.imw_measurement)
    #  @api.multi
    #  @api.onchange('product_id')
    # def _value_pc(self):
#    self.otherUnitMeasure = self.product_id.otherUnitMeasure


 
