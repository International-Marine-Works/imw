# -*- coding: utf-8 -*-

from odoo import models, fields, api
# from odoo import api, fields, models, _
# from odoo.addons import decimal_precision as dp
# from odoo.exceptions import UserError
# from odoo.tools import float_utils
import logging
_logger = logging.getLogger(__name__)

class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    referenceRecive = fields.Char(string='R Reference', states={'open': [('readonly', False)]}, copy=False,
                           readonly=True,
                          help="Used to hold the reference of the external mean that created this statement (name of imported file, reference of online synchronization...)")

class  SaleOrder(models.Model):
    _inherit = 'sale.order'



    @api.multi
    def sale_order_alltotalhide(self):

        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        return self.env.ref('sale.action_report_saleorder') \
            .with_context({'discard_logo_check': True}).report_action(self,data=1)



    def sale_order_totalhide(self):

        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        return self.env.ref('sale.action_report_saleorder') \
            .with_context({'discard_logo_check': True}).report_action(self,data=2)



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    imw_qty = fields.Float(string='Quantity')
    imw_measurement = fields.Float(string='Measurement',default=1)
    category_id = fields.Many2one('product.category', 'category')
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id

        if not account and self.product_id:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos and account:

            account = fpos.map_account(account)

        res = {
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'display_type': self.display_type,
            'imw_qty':self.imw_qty,
            'imw_measurement':self.imw_measurement,
            'otherUnitMeasure':self.otherUnitMeasure.id,
            'category_id':self.category_id,
        }
        return res

    @api.multi
    @api.onchange('imw_qty','imw_measurement')
    def _ChangeQty(self):
        if float(self.imw_measurement) == 0 :
           self.imw_measurement = 1

        self.product_uom_qty = float(self.imw_qty) * float(self.imw_measurement)


    @api.multi
    @api.onchange('product_uom_qty')
    def _change_uom_qty(self):
        if float(self.imw_measurement) == 0:
            self.imw_measurement = 1
        #self.product_uom_qty = float(self.imw_qty) * float(self.imw_measurement)
        imwQty = float(self.imw_qty) if float(self.imw_qty) > 0 else 1
        self.imw_measurement = float(self.product_uom_qty) /   imwQty


    @api.multi
    @api.onchange('product_id')
    def _onchangeProductId(self):
        self.product_uom_change()
        self.otherUnitMeasure = self.product_id.otherUnitMeasure
        if float(self.imw_measurement) == 0:
            self.imw_measurement = 1

        if float(self.imw_qty) == 0:
            self.imw_qty = 1
        if float(self.product_uom_qty) == 0:
            self.product_uom_qty = 1

    @api.onchange('product_uom')#, 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product),
                                                                                      product.taxes_id, self.tax_id,
                                                                                      self.company_id)

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


    #@api.onchange('product_id')
    #def onchange_product(self):
        # res = {}
        # If no UoM or incorrect UoM put default one from product
        # if self.product_id:
        #   self.product_uom_id = self.product_id.uom_id
        #  res['domain'] = {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
# return res

class imw_product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    otherUnitMeasure = fields.Many2one('uom.uom', 'Other Unit of Measure')

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


