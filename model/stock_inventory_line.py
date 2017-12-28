# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class stock_inventory_line(models.Model):
    _inherit = 'stock.inventory.line'
    