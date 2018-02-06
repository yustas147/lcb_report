# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class pos_order_line(models.Model):
    _name = 'pos.order.line'
    _inherit = ['pos.order.line','lcb.base']
    
    @api.multi
    def _get_pack_lots(self):
        spol_env = self.env['stock.pack.operation.lot']
        for inst in self:
            stock_pack_operation_lots = spol_env.search([('date_received', '=', inst.sale_date)])
            if len(stock_pack_operation_lots):
                inst.pack_lot_ids = unicode(','.join([x.lot_id.name for x in stock_pack_operation_lots if inst.product_id == x.lot_id.product_id]))
            else:
                inst.pack_lot_ids = inst.product_id.barcode

    @api.depends('product_price_no_tax')
    def _get_tax_amount(self):
        tax_marijuana_037 = 0.37
        for inst in self:
            ######################################## eto kostyl vremenno
            inst.tax_amount =  inst.product_price_no_tax * tax_marijuana_037
    
    @api.multi
    def _get_product_price_no_tax(self):
        total_tax_coeff = 0.37 + 0.076
        for inst in self:
            PT = inst.price_subtotal_incl * total_tax_coeff
            inst.prduct_price_no_tax = inst.price_subtotal_incl - PT     
   
    pack_lot_ids = fields.Char(string="Pack lot ids", compute='_get_pack_lots')
    sale_date = fields.Datetime(string="Sale Date", related='order_id.date_order', store=True)
    tax_amount = fields.Float(string="Total Excise Tax", compute='_get_tax_amount',  store=False)
    product_price_no_tax = fields.Float(string="Total Price", compute='_get_product_price_no_tax', store=False)
    