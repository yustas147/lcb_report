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
            
    
    @api.depends('product_price_no_tax')
    def _get_tax_amount(self):
        tax_marijuana_037 = 0.37
        for inst in self:
            ######################################## eto kostyl vremenno
#            inst.tax_amount = inst.price_tax - inst.price_subtotal*0.076
            inst.tax_amount =  inst.product_price_no_tax * tax_marijuana_037
#            inst.tax_amount = (inst.price_subtotal_incl - inst.price_subtotal)*1.084    
#            inst.tax_amount = inst.price_subtotal_incl - inst.price_subtotal*1.084    

    @api.multi
    def _get_product_price_no_tax(self):
        total_tax_coeff = 0.37 + 0.076
        for inst in self:
            PT = inst.price_subtotal_incl * total_tax_coeff
            inst.prduct_price_no_tax = inst.price_subtotal_incl - PT 
            
    #@api.multi
    #def _get_pp_tax(self):
        #tax_marijuana_037 = 0.37
        #sales_tax_0076 = 0.076
        #total_tax_coeff = tax_marijuana_037 + sales_tax_0076
        #for inst in self:
            #PT = inst.price_subtotal_incl * total_tax_coeff
            #inst.prduct_price_no_tax = inst.price_subtotal_incl - PT 
            #inst.tax_amount =  inst.product_price_no_tax * tax_marijuana_037
             
            

    
    license_number = fields.Char(string="License #", compute='_get_license_number')
    is_medical = fields.Boolean(string="Medical Sale?", compute='_check_med', store=False)
    #tax_amount = fields.Float(string="Total Excise Tax", compute='_get_pp_tax', digits=None, store=True)
    #product_price_no_tax = fields.Float(string="Total Price", compute='_get_pp_tax', digits=None, store=True)
    tax_amount = fields.Float(string="Total Excise Tax", compute='_get_tax_amount',  store=False)
    product_price_no_tax = fields.Float(string="Total Price", compute='_get_product_price_no_tax', store=False)
    #tax_amount = fields.Float(string="Total Excise Tax", compute='get_tax_amount', digits=None)
    #sale_date = fields.Datetime(string="Sale Date", related='order_id.date_order', store=True)
    
    #is_medical = fields.Boolean(string="Medical Sale?")
    