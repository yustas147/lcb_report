# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit='sale.order'
    
    @api.multi
    def amount_line_tax(self, line, context=None):
        for inst in self:
            return inst._amount_line_tax(line)

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    @api.multi
    def get_tax_amount(self):
        for inst in self:
            inst.tax_amount = inst.order_id.amount_line_tax(inst)
            
    @api.multi 
    def _get_license_number(self):
        company = self.env['res.company'].browse(self.env['res.company']._company_default_get('lcb_report'))
        for inst in self:
            inst.license_number = company.api_license_number
            
    
    license_number = fields.Char(string="License #", compute='_get_license_number')
    tax_amount = fields.Float(string="Total Excise Tax", compute='get_tax_amount', digits=None)
    sale_date = fields.Date(string="Sale Date", related='order_id.date_confirm', store=True)
    
    is_medical = fields.Boolean(string="Medical Sale?")
    