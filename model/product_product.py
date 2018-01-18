# -*- coding: utf-8 -*-
from openerp import models, fields, api
#from openerp.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

#class sale_order(models.Model):
    #_inherit='sale.order'
    
    #@api.multi
    #def amount_line_tax(self, line, context=None):
        #for inst in self:
            #return inst._amount_line_tax(line)

class product_product(models.Model):
    _inherit='product.product'
    
    lot_ids = fields.One2many(comodel_name='stock.production.lot', inverse_name='product_id', string='Stock Lots')
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        argss = [] if args is None else args
        if not (name == '' and operator == 'ilike'):
            argss += ['|','|',('name', operator, name), ('lot_ids.name',operator, name),('barcode', operator, name)]
        return super(product_product, self).name_search(name='', operator='ilike', args=argss, limit=limit, name_get_uid=name_get_uid)
            
    