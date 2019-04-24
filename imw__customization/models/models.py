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




  # @api.model
  # def _selection_filter(self):
  #     """ Get the list of filter allowed according to the options checked
  #     in 'Settings\Warehouse'. """
  #     records.filtered(lambda r: r.company_id == user.company_id)
  #     res_filter = [
  #         ('none', _('All products')),
  #         ('category', _('One product category')),
  #         ('product', _('One product only')),
  #         ('partial', _('Select products manually'))]

  #     if self.user_has_groups('stock.group_tracking_owner'):
  #         res_filter += [('owner', _('One owner only')), ('product_owner', _('One product for a specific owner'))]
  #     if self.user_has_groups('stock.group_production_lot'):
  #         res_filter.append(('lot', _('One Lot/Serial Number')))
  #     if self.user_has_groups('stock.group_tracking_lot'):
  #         res_filter.append(('pack', _('A Pack')))
  #     return res_filter

  # @api.onchange('filter')
  # def onchange_filter(self):
  #     if self.filter not in ('product', 'product_owner'):
  #         self.product_id = False
  #     if self.filter not in ('owner', 'product_owner'):
  #         self.package_id = False
  #     if self.filter != 'category':
  #         self.category_id = False
  #     if self.filter == 'product':
  #         self.exhausted = True


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










