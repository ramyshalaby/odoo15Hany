from odoo import api, fields, models, _, SUPERUSER_ID, tools
import logging
from . import api_global_function

_logger = logging.getLogger(__name__)
DATES_FORMAT = "%Y-%m-%d"
class sale_order(models.Model):
    _inherit = "sale.order"

    come_from = fields.Char('Come From')
    api_sale_order_state = fields.Selection(
        [
            ('cancel','Cancelled'),
            ('cancelReversal', 'Canceled Reversal'),
            ('chargeback', 'Chargeback'),
            ('complete', 'Complete'),
            ('denied', 'Denied'),
            ('expired', 'Expired'),
            ('failed', 'Failed'),
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('processing', 'Processing'),
            ('refunded', 'Refunded'),
            ('reversed', 'Reversed'),
            ('shipped', 'Shipped'),
            ('voided', 'Voided'),
            ('payed', 'Payed'),
        ]
    , default='pending')
    @api.model
    def get_sale_order_info(self, **args):
        lang = args.get('lang')
        if lang == 'ar':
            lang = 'ar_SY'
        elif lang == 'en':
            lang = 'en_US'
        else:
            return api_global_function.return_failed_request_vals("Wrong Language Name", "عفوا اللغه غير مدعومه")
        domain = []
        if args.get("customer_id", False):
            domain.append(('partner_id', '=', args.get("customer_id", False)))
        if args.get("order_id", False):
            domain.append(('id', '=', args.get("order_id", False)))

        sale_order_objs = self.env['sale.order'].sudo().search(domain)
        result = []
        for sale_order_obj in sale_order_objs:
            order_line_list = []
            for sale_order_line_obj in sale_order_obj.order_line:
                order_line_list.append({
                    'sale_line_id': sale_order_line_obj.id,
                    'product': {"id":sale_order_line_obj.product_id.id, 'name':  sale_order_line_obj.product_id.name} if sale_order_line_obj.product_id else {},
                    "name": sale_order_line_obj.name,
                    'quantity':sale_order_line_obj.product_uom_qty,
                    'delivered':sale_order_line_obj.qty_delivered,
                    'invoiced': sale_order_line_obj.qty_invoiced,
                    'unit_of_measure': {"id":sale_order_line_obj.product_uom.id, 'name':  sale_order_line_obj.product_uom.name} if sale_order_line_obj.product_uom else {},
                    'unit_price': sale_order_line_obj.price_unit,
                    'discount%': sale_order_line_obj.discount,
                    'price_total': sale_order_line_obj.price_total,
                    # 'cost': sale_order_line_obj.purchase_price,
                    'margin':  sale_order_line_obj.margin,
                    'margin_percent%': sale_order_line_obj.margin_percent,
                })
            result.append({
                'id': sale_order_obj.id,
                'name': sale_order_obj.name or '',
                'customer': {'id': sale_order_obj.partner_id.id, 'name':  sale_order_obj.partner_id.name} if  sale_order_obj.partner_id else {},
                'date_order': sale_order_obj.date_order or '',
                'amount_total': sale_order_obj.amount_total,
                'margin':sale_order_obj.margin,
                'tax_amount':sale_order_obj.amount_tax,
                'untaxed_amount':sale_order_obj.amount_untaxed,
                'come_from':sale_order_obj.come_from or 'Odoo',
                'order_status': dict(sale_order_obj._fields['state'].selection).get(sale_order_obj.state),
                'online_sale_state': dict(sale_order_obj._fields['api_sale_order_state'].selection).get(sale_order_obj.api_sale_order_state),
                "order_line_list": order_line_list
            })
        return api_global_function.return_success_list_api(result)

    def check_saleorder_vals(self, args):
        sale_order_vals = {}
        if args.get("RequestID", False):
            sale_order_vals.update({'id': args.get("RequestID", False)})
        try:
            if not args.get('partner_id', False):
                return False, api_global_function.return_failed_request_vals("Customer ID Not provided",
                                                                             "عفوا العميل مش موجود")
            if not self.env['res.partner'].sudo().search([('id','=',args.get('partner_id', False))]):
                return False, api_global_function.return_failed_request_vals("Customer ID Not Correct",
                                                                             "عفوا العميل غير صحيح")
            sale_order_vals.update({'partner_id': args.get("partner_id", False)})
            if not args.get('come_from', False):
                return False, api_global_function.return_failed_request_vals("Come From Not provided",
                                                                             "عفوا المصدر مش موجود")
            sale_order_vals.update({'come_from': args.get('come_from', False)})

            if args.get('date_order', False):
                sale_order_vals.update({'date_order': args.get("date_order", False)})
            if not args.get('order_line', []):
                return False, api_global_function.return_failed_request_vals("Sales order lines is empty please check",
                                                                             "عفوا امر البيع خالى من المنتجات ")
            sale_order_line_dic={}
            sale_order_line_list = []
            for sale_order_line in args.get('order_line', []):
                sale_order_line_dic = {}
                if not sale_order_line.get('product_id', False):
                    return False, api_global_function.return_failed_request_vals(
                        "Sales order lines product is empty please check",
                        "عفوا امر البيع خالى من المنتجات ")
                if not self.env['product.product'].sudo().search([('id', '=', sale_order_line.get('product_id', False))]):
                    return False, api_global_function.return_failed_request_vals("Product ID Not Correct",
                                                                                 "عفوا المنتج غير صحيح")
                sale_order_line_dic['product_id'] = sale_order_line.get('product_id', False)
                if not sale_order_line.get('product_quantity', False):
                    return False, api_global_function.return_failed_request_vals(
                        "Sales order lines product Quantity is not provided",
                        "عفواالكميه الخاصه بالمنتج غير موجودة ")
                if sale_order_line.get('product_quantity', False) <= 0.0:
                    return False, api_global_function.return_failed_request_vals(
                        "Sales order lines product Quantity must be greater than Zero",
                        "عفواالكميه الخاصه بالمنتج لابد ان تكون اكبر من الزيرو ")
                sale_order_line_dic['product_uom_qty'] = sale_order_line.get('product_quantity', False)
                if not sale_order_line.get('unit_price', False):
                    return False, api_global_function.return_failed_request_vals(
                        "Sales order lines product price is not provided",
                        "عفوا سعر الخاص بالمنتج غير موجودة ")
                if sale_order_line.get('unit_price', False) <= 0.0:
                    return False, api_global_function.return_failed_request_vals(
                        "Sales order lines product price must be greater than Zero",
                        "عفوا السعر الخاص بالمنتج لابد ان تكون اكبر من الزيرو ")
                sale_order_line_dic['price_unit'] = sale_order_line.get('unit_price', False)
                sale_order_line_list.append((0, 0, sale_order_line_dic))
            sale_order_vals.update({'order_line': sale_order_line_list})
        except Exception as e:
            arabic_message = "%s  " % _(str(e)),
            englishmessage = "%s." % _(str(e))
            return False, api_global_function.return_failed_request_vals(englishmessage, arabic_message)
        return True, sale_order_vals


    def add_update_sale_order(self, **args):
        request_id = args.get("RequestID", False)
        check_vals, sale_order_vals = self.check_saleorder_vals(args)
        if not check_vals:
            return sale_order_vals
        try:
            if not request_id:
                sale_order_obj = self.with_user(args.get('userId')).sudo().create(sale_order_vals)
            else:
                #Update Request ID
                sale_order_obj = self.with_user(args.get('userId')).sudo().browse(request_id)
                sale_order_obj.with_user(args.get('userId')).sudo().write(sale_order_vals)
        except Exception as e:
            self.env.cr.rollback()
            return api_global_function.return_failed_api(_(str(e)))
        if not request_id:
            return api_global_function.return_success_creation_api(sale_order_obj.id, sale_order_obj.id)
        else:
            return api_global_function.return_success_update_api(sale_order_obj.id, sale_order_obj.id)

    def change_sale_order_status(self, **args):
        if not args.get("sale_order_id", False):
            return False, api_global_function.return_failed_request_vals(
                "Sales order ID is empty please check",
                "عفوا رقم امر البيع غير موجود ")
        try:
            sale_order_obj = self.with_user(args.get('userId')).sudo().browse(int(args.get("sale_order_id", False)))
            if not args.get("sale_status", False):
                return False, api_global_function.return_failed_request_vals(
                    "Sales order Status is not provided please check",
                    "عفوا حالة امر البيع غير موجود ")
            if args.get("sale_status", False) not in ['cancel','cancelReversal','chargeback', 'complete', 'denied', 'expired', 'failed', 'pending', 'processed',
                                                      'processing', 'refunded', 'reversed', 'shipped', 'voided', 'payed']:
                return False, api_global_function.return_failed_request_vals(
                    "Sales order Status is not Correct please check",
                    "عفوا حالة امر البيع غير صحيحة ")
            sale_order_obj.with_user(args.get('userId')).sudo().write({'api_sale_order_state':args.get("sale_status", False)})
        except Exception as e:
            self.env.cr.rollback()
            return api_global_function.return_failed_api(_(str(e)))
        return api_global_function.return_success_update_api(sale_order_obj.id, sale_order_obj.id)


