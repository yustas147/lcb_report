# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class sale_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line','lcb.base']
    
    @api.multi
    def _get_tax_amount(self):
        for inst in self:
            inst.tax_amount = inst.price_tax - inst.price_subtotal*0.076
#            inst.tax_amount = inst.price_tax - inst.price_subtotal*0.084
            
    @api.multi
    def _get_pack_lots(self):
        spol_env = self.env['stock.pack.operation.lot']
        for inst in self:
            stock_pack_operation_lots = spol_env.search([('date_received', '=', inst.sale_date)])
            if len(stock_pack_operation_lots):
                inst.pack_lot_ids = stock_pack_operation_lots.lot_id.name
   
    pack_lot_ids = fields.Char(string="Pack lot ids", compute='_get_pack_lots')            
    sale_date = fields.Datetime(string="Sale Date", related='order_id.date_order', store=True)
    
#    license_number = fields.Char(string="License #", compute='_get_license_number')
#    tax_amount = fields.Float(string="Total Excise Tax", compute='_get_tax_amount', digits=None)
#    sale_date = fields.Date(string="Sale Date", related='order_id.date_confirm', store=True)
    
#    is_medical = fields.Boolean(string="Medical Sale?")
    