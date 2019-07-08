# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

from num2words import num2words


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _description = "Invoice"

    @api.multi
    def amount_to_word(self, amount):
        return num2words(amount, lang='en').title()


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

# Adding Reference 2 field in Model account.move as an optional field dtd:2019-06-26
class JournalEntriesRef2(models.Model):
    _inherit='account.move'

    imw_ref2=fields.Char('Reference2')


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


