# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_utils
import logging
_logger = logging.getLogger(__name__)

class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    referenceRecive = fields.Char(string='R Reference', states={'open': [('readonly', False)]}, copy=False,
                           readonly=True,
                          help="Used to hold the reference of the external mean that created this statement (name of imported file, reference of online synchronization...)")
  
class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    imw_qty = fields.Float(string='Quantity')
    imw_measurement = fields.Float(string='Measurement',default=1)
    category_id = fields.Many2one('product.category', 'category')
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')

    @api.multi
    @api.onchange('imw_qty', 'imw_measurement')
    def _ChangeQty(self):
         if float(self.imw_measurement) == 0:
            self.imw_measurement = 1

         self.quantity = float(self.imw_qty) * float(self.imw_measurement)






    @api.multi
    @api.onchange('product_id')
    def _onchangeProductId(self):
        self.otherUnitMeasure = self.product_id.otherUnitMeasure

        if float(self.imw_qty) == 0:
            self.imw_qty = 1

        if float(self.imw_measurement) == 0:
            self.imw_measurement = 1
            # self.product_uom_qty = float(self.imw_qty) * float(self.imw_measurement)
        imwQty = float(self.imw_qty) if float(self.imw_qty) > 0 else 1
        self.imw_measurement = float(self.quantity) / imwQty


