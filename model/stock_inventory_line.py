# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class stock_inventory_line(models.Model):
    _inherit = 'stock.inventory.line'
    
    @api.multi
    def _qty_lost_gained(self):
        for inst in self:
            inst.quantity_lost_gained =   inst.product_qty - inst.theoretical_qty
            
    @api.multi 
    def _get_license_number(self):
        #user_id  = self.env['res.user'].browse()
        company = self.env['res.company'].browse(self.env['res.company']._company_default_get('lcb_report'))
        for inst in self:
            inst.license_number = company.api_license_number
            
    license_number = fields.Char(string="License #", compute='_get_license_number')
    #license_number = lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('lcb_report')).api_license_number
    adjustment_date = fields.Datetime(string="Adjustment Date", related='inventory_id.date')
#    inventory_type = fields.Char(related='prod_lot_id.name', string="Inventory Type", store=True)
#    inventory_type = fields.Char(related='prod_lot_id.product_id.product_tmpl_id.inventory_type_id.name', string="Inventory Type", store=True)
    inventory_type = fields.Char(related='prod_lot_id.product_id.inventory_type_id.name', string="Inventory Type", store=False)
    quantity_lost_gained = fields.Float(string="Quantity Lost/Gained (+/-)", compute='_qty_lost_gained', digits=None)
    adjustment_reason = fields.Selection(string='Adjustment Reason', related='inventory_id.type_reason')
    additional_explanation = fields.Char(string='Additional Explanation', related='inventory_id.description')
    