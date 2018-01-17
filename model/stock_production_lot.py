# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

#class sale_order(models.Model):
    #_inherit='sale.order'
    
    #@api.multi
    #def amount_line_tax(self, line, context=None):
        #for inst in self:
            #return inst._amount_line_tax(line)

class stock_production_lot(models.Model):
    _inherit='stock.production.lot'
    
    @api.constrains('name')
    def _check_lot_name(self):
        company = self.env['res.company']._company_default_get('lcb_report')
        for inst in self:
            l = self.search([('name','=',inst.name)])
            if len(l) >1:
                raise ValidationError("Lot number should be unique. Please correct this %s" % inst.name)
            elif len(inst.name) != 16:
                raise ValidationError("Lot number should have 16 digit length. Please correct this %s" % inst.name)
            elif inst.name[:6] != company.api_license_number:
                raise ValidationError("Lot number should start with company license number %s. \
                For example: %sxxxxxxxxxx, where x is a digit [0-9]. Please insert correct lot number." % (company.api_license_number,company.api_license_number))
            
    