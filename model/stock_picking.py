# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class stock_pack_operation(models.Model):
    _inherit = 'stock.pack.operation'
    
    @api.multi 
    def _get_license_number(self):
        company = self.env['res.company'].browse(self.env['res.company']._company_default_get('lcb_report'))
        for inst in self:
            inst.license_number = company.api_license_number
            
    
    @api.multi
    def _get_total_price(self):
        for inst in self:
            inst.total_price = inst.product_id.standard_price * inst.product_qty
            
    license_number = fields.Char(string="License #", compute='_get_license_number')
    origin_license = fields.Char(string="Origin License #", related='picking_id.partner_id.partner_license_key')
    date_received = fields.Datetime(string="Date Received", related='picking_id.date_done', store=True)
    
    inventory_type = fields.Char(related='lot_id.product_id.inventory_type_id.name', string="Inventory Type", store=False)    
    strain  = fields.Char(related='lot_id.product_id.name_template', string="Strain", store=False)      
#    strain  = fields.Char(related='lot_id.product_id.strain_id.name', string="Strain", store=False)      
    #lquantity = fields.Float(string="Quantity")    
    total_price = fields.Float(string="Total price", compute="_get_total_price")