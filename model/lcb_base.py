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

class lcb_base(models.Model):
    _name='lcb.base'
    
    #@api.multi
    #def get_tax_amount(self):
        #for inst in self:
            #inst.tax_amount = inst.price_tax - inst.price_subtotal*0.084
            
    @api.multi
    def _check_med(self):
        for inst in self:
            if inst.tax_amount < 0.00001:
                inst.is_medical = True
            else:
                inst.is_medical = False
    
    @api.multi 
    def _get_license_number(self):
        company = self.env['res.company']._company_default_get('lcb_report')
#        company = self.env['res.company'].browse(self.env['res.company']._company_default_get('lcb_report'))
        for inst in self:
            inst.license_number = company.api_license_number
            
    @api.multi
    def _get_tax_amount(self):
        for inst in self:
            ######################################## eto kostyl vremenno
            inst.tax_amount = inst.price_subtotal_incl - inst.price_subtotal*1.084    

    
    license_number = fields.Char(string="License #", compute='_get_license_number')
    is_medical = fields.Boolean(string="Medical Sale?", compute='_check_med', store=False)
    tax_amount = fields.Float(string="Total Excise Tax", compute='_get_tax_amount', digits=None)
    #tax_amount = fields.Float(string="Total Excise Tax", compute='get_tax_amount', digits=None)
    #sale_date = fields.Datetime(string="Sale Date", related='order_id.date_order', store=True)
    
    #is_medical = fields.Boolean(string="Medical Sale?")
    