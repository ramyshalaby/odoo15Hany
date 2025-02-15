# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api,fields,models,_

class ProjectTask(models.Model):
    _inherit="project.task"
    _description = "Project Task"

    sale_order_id = fields.Many2one('sale.order', string='Source Sale Order', readonly=True, help='This field displays customer name')
    sale_order_date = fields.Date(string='Order Date',help='This field displays confirm order date')
    products_task_ids = fields.Many2many('product.product','product_id',string='Products',help='This field displays products of the specific order')
