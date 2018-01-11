# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

#class sale_order(models.Model):
    #_inherit='sale.order'
    
    #@api.multi
    #def amount_line_tax(self, line, context=None):
        #for inst in self:
            #return inst._amount_line_tax(line)

class pos_order_line(models.Model):
    _inherit = 'pos.order.line'
    
    @api.multi
    def get_tax_amount(self):
        for inst in self:
            ######################################## eto kostyl vremenno
            inst.tax_amount = inst.price_subtotal_incl - inst.price_subtotal*1.084
#            inst.tax_amount = inst.order_id.amount_line_tax(inst)
            
    @api.multi 
    def _get_license_number(self):
        company = self.env['res.company']._company_default_get('lcb_report')
#        company = self.env['res.company'].browse(self.env['res.company']._company_default_get('lcb_report'))
        for inst in self:
            inst.license_number = company.api_license_number
            
    @api.multi
    def _get_pack_lots(self):
        spol_env = self.env['stock.pack.operation.lot']
        for inst in self:
            stock_pack_operation_lots = spol_env.search([('date_received', '=', inst.sale_date)])
            if len(stock_pack_operation_lots):
                inst.pack_lot_ids = stock_pack_operation_lots.lot_id.name
    @api.multi
    def _check_med(self):
        for inst in self:
            if inst.tax_amount < 0.00001:
                inst.is_medical = True
            else:
                inst.is_medical = False
                
    
        
    license_number = fields.Char(string="License #", compute='_get_license_number')
    tax_amount = fields.Float(string="Total Excise Tax", compute='get_tax_amount', digits=None)
    sale_date = fields.Datetime(string="Sale Date", related='order_id.date_order', store=True)
#    sale_date = fields.Date(string="Sale Date", related='order_id.date_confirm', store=True)
    
    is_medical = fields.Boolean(string="Medical Sale?", compute='_check_med', store=False)
    pack_lot_ids = fields.Char(string="Pack lot ids", compute='_get_pack_lots')
    