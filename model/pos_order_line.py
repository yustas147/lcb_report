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
    
   
    pack_lot_ids = fields.Char(string="Pack lot ids", compute='_get_pack_lots')
    sale_date = fields.Datetime(string="Sale Date", related='order_id.date_order', store=True)
    