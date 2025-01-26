from odoo import api, fields, models, _, SUPERUSER_ID, tools
import logging
from . import api_global_function

_logger = logging.getLogger(__name__)
DATES_FORMAT = "%Y-%m-%d"


class product_template(models.Model):
    _inherit = "product.template"

    come_from = fields.Char('Come From')
    product_images_ids = fields.One2many('product.images', 'product_id', 'Images')
    x_sku = fields.Char('SKU')
    x_fast_number = fields.Char('Fast Number')
    x_serial_number = fields.Char('Serial Number')


class product_template(models.Model):
    _inherit = "product.product"

    @api.model
    def get_product_info(self, **args):
        lang = args.get('lang')
        if lang == 'ar':
            lang = 'ar_SY'
        elif lang == 'en':
            lang = 'en_US'
        else:
            return api_global_function.return_failed_request_vals("Wrong Language Name", "عفوا اللغه غير مدعومه")
        domain = []
        if args.get("product_id", False):
            domain.append(('id', '=', args.get("product_id", False)))
        if args.get("product_type", False):
            if args.get("product_type", False) not in ['consu', 'service', 'product', 'event']:
                return api_global_function.return_failed_request_vals(
                    "Wrong Product Type it must be 'consu (Consumable)',"
                    "'service(Service)','product(Storable Product)','event(Event Ticket)'",
                    "عفوا نوع المنتج غير صحيح")
            domain.append(('detailed_type', '=', args.get("product_type", False)))
        if args.get("categ_id", False):
            if not self.env['product.category'].sudo().search([('id', '=', args.get("categ_id", False))]):
                return api_global_function.return_failed_request_vals(
                    "Wrong Category ID Please Cjeck",
                    "عفوا تصنيف المنتج غير صحيح")
            domain.append(('categ_id', '=', args.get("categ_id", False)))

        product_template_objs = self.env['product.product'].sudo().search(domain)
        result = []
        for product_template_obj in product_template_objs:
            product_images_list = []
            for product_images_obj in product_template_obj.product_images_ids:
                product_images_list.append(product_images_obj.image_link)
            result.append({
                'id': product_template_obj.id,
                'product_tmpl_id': product_template_obj.product_tmpl_id.id,
                'name': product_template_obj.name or '',
                'image': product_template_obj.image_1920 or '',
                'fullname': product_template_obj.display_name or '',
                'can_be_sold': product_template_obj.sale_ok,
                'can_be_purchase': product_template_obj.purchase_ok,
                'product_type': product_template_obj.detailed_type,
                # 'invoicing_policy': product_template_obj.service_policy,
                'invoice_policy': product_template_obj.invoice_policy,
                # 'product_type': dict(product_template_obj._fields['detailed_type'].selection).get(product_template_obj.detailed_type),
                # 'invoicing_policy': dict(product_template_obj._fields['service_policy'].selection).get(product_template_obj.service_policy),
                # 'expense_policy': dict(product_template_obj._fields['expense_policy'].selection).get(product_template_obj.expense_policy),
                'unit_of_measure': {'id': product_template_obj.uom_id.id,
                                    'name': product_template_obj.uom_id.name} if product_template_obj.uom_id else {},
                'sales_price': product_template_obj.list_price,
                # 'cost_price': product_template_obj.standard_price,
                'currency': {'id': product_template_obj.currency_id.id,
                             'name': product_template_obj.currency_id.name} if product_template_obj.currency_id else {},
                'cost_currency': {'id': product_template_obj.cost_currency_id.id,
                                  'name': product_template_obj.cost_currency_id.name} if product_template_obj.cost_currency_id else {},
                'product_category': {'id': product_template_obj.categ_id.id,
                                     'name': product_template_obj.categ_id.name} if product_template_obj.categ_id else {},
                'internal_reference': product_template_obj.default_code or '',
                'barcode': product_template_obj.barcode or '',
                # 'product_brand': {'id': product_template_obj.brand_id.id, 'name': product_template_obj.brand_id.name} if product_template_obj.brand_id else {},
                # 'product_group': {'id': product_template_obj.group_id.id, 'name': product_template_obj.group_id.name} if product_template_obj.group_id else {},
                'sale_description': product_template_obj.description_sale,
                'purchase_description': product_template_obj.description_purchase,
                # 'weight': product_template_obj.weight,
                # 'volume': product_template_obj.volume,
                'come_from': product_template_obj.come_from or 'Odoo',
                'product_images_list': product_images_list,
                'quantity_on_hand': product_template_obj.qty_available,
                'sku': product_template_obj.x_sku or '',
                'fast_number': product_template_obj.x_fast_number or '',
                'serial_number': product_template_obj.x_serial_number or '',
            })
        return api_global_function.return_success_list_api(result)

    def check_product_vals(self, args):
        product_vals = {'detailed_type': 'product'}
        if args.get("RequestID", False):
            product_vals.update({'id': args.get("RequestID", False)})
            if args.get('barcode', False):
                if self.env['product.product'].sudo().search([('barcode', '=', args.get('barcode', False))]):
                    return False, api_global_function.return_failed_request_vals(
                        "Product Barcode can only be assigned to one product",
                        "عفوا باركود المنتج موجود مسبقا")
                product_vals.update({'barcode': args.get('barcode', False)})
        try:
            if not args.get('name', False) and not args.get("RequestID", False):
                return False, api_global_function.return_failed_request_vals("Product Name Not provided",
                                                                             "عفوا اسم المنتج مش موجود")
            if args.get('name', False):
                product_vals.update({'name': args.get('name', False)})
            if not args.get('come_from', False) and not args.get("RequestID", False):
                return False, api_global_function.return_failed_request_vals("Come From Not provided",
                                                                             "عفوا المصدر مش موجود")
            if args.get('come_from', False):
                product_vals.update({'come_from': args.get('come_from', False)})

            if args.get('product_type', False):
                if args.get("product_type", False) not in ['consu', 'service', 'product', 'event']:
                    return api_global_function.return_failed_request_vals(
                        "Wrong Product Type it must be 'consu (Consumable)',"
                        "'service(Service)','product(Storable Product)','event(Event Ticket)'",
                        "عفوا نوع المنتج غير صحيح")
                product_vals.update({'detailed_type': args.get('product_type', False)})
            if not args.get('sale_price', False) and not args.get("RequestID", False):
                return False, api_global_function.return_failed_request_vals("Product Sale Price Not provided",
                                                                             "عفوا سعر البيع للمنتج مش موجود")
            if args.get('sale_price', False):
                product_vals.update({'list_price': args.get('sale_price', False)})
            if not args.get('internal_reference', False) and not args.get("RequestID", False):
                return False, api_global_function.return_failed_request_vals("Product internal reference Not provided",
                                                                             "عفوا الرقم المرجعى للمنتج مش موجود")
            if args.get('internal_reference', False):
                product_vals.update({'default_code': args.get('internal_reference', False)})
            if not args.get('barcode', False) and not args.get("RequestID", False):
                return False, api_global_function.return_failed_request_vals("Product Barcode Not provided",
                                                                             "عفوا باركود المنتج مش موجود")
            if args.get('barcode', False):
                if self.env['product.product'].sudo().search([('barcode', '=', args.get('barcode', False))]):
                    return False, api_global_function.return_failed_request_vals(
                        "Product Barcode can only be assigned to one product",
                        "عفوا باركود المنتج موجود مسبقا")
                product_vals.update({'barcode': args.get('barcode', False)})
            if args.get('sale_description', False):
                product_vals.update({'description_sale': args.get('sale_description', False)})
            if args.get('purchase_description', False):
                product_vals.update({'description_purchase': args.get('purchase_description', False)})
            if args.get('image', False):
                product_vals.update({'image_1920': args.get('image', False)})
            if args.get('sku', False):
                product_vals.update({'x_sku': args.get('sku', False)})
            if args.get('fast_number', False):
                product_vals.update({'x_fast_number': args.get('fast_number', False)})
            if args.get('serial_number', False):
                product_vals.update({'x_serial_number': args.get('serial_number', False)})

        except Exception as e:
            arabic_message = "%s  " % _(str(e)),
            englishmessage = "%s." % _(str(e))
            return False, api_global_function.return_failed_request_vals(englishmessage, arabic_message)
        return True, product_vals

    def add_update_product(self, **args):
        request_id = args.get("RequestID", False)
        check_vals, product_vals = self.check_product_vals(args)
        if not check_vals:
            return product_vals
        try:
            if not request_id:
                product_template_obj = self.with_user(args.get('userId')).sudo().create(product_vals)
            else:
                # Update Request ID
                product_template_obj = self.with_user(args.get('userId')).sudo().browse(request_id)
                product_template_obj.with_user(args.get('userId')).sudo().write(product_vals)
            if args.get('product_images', []):
                for product_images in args.get('product_images', []):
                    if not product_images.get('image_link', False):
                        return False, api_global_function.return_failed_request_vals(
                            "Product Image Link is not provided",
                            "عفوا لينك الصورة بالمنتج غير موجودة ")
                    product_template_image_obj = self.env['product.images'].with_user(args.get('userId')).sudo().create(
                        {"product_id": product_template_obj.product_tmpl_id.id,
                         "image_link": product_images.get('image_link', "")})
                    # product_images_dic['image_link'] = product_images.get('image_link', False)
                    # product_images_list.append((0, 0, product_images_dic))
                # product_vals.update({'product_images_ids': product_images_list})
        except Exception as e:
            self.env.cr.rollback()
            return api_global_function.return_failed_api(_(str(e)))
        if not request_id:
            return api_global_function.return_success_creation_api(product_template_obj.id, product_template_obj.id)
        else:
            return api_global_function.return_success_update_api(product_template_obj.id, product_template_obj.id)

    def add_product_image(self, **args):
        if not args.get("product_id", False):
            return False, api_global_function.return_failed_request_vals(
                "Product ID is empty please check",
                "عفوا رقم الصنف غير موجود ")
        try:
            product_product_obj = self.with_user(args.get('userId')).sudo().browse(int(args.get("product_id", False)))
            if not args.get('product_images', []):
                return False, api_global_function.return_failed_request_vals(
                    "Product Images is empty please check",
                    "عفوا صور الصنف غير موجود ")
            if args.get('product_images', []):
                for product_images in args.get('product_images', []):
                    if not product_images.get('image_link', False):
                        return False, api_global_function.return_failed_request_vals(
                            "Product Image Link is not provided",
                            "عفوا لينك الصورة بالمنتج غير موجودة ")
                    product_template_image_obj = self.env['product.images'].with_user(args.get('userId')).sudo().create(
                        {"product_id": product_product_obj.product_tmpl_id.id,
                         "image_link": product_images.get('image_link', "")})
        except Exception as e:
            self.env.cr.rollback()
            return api_global_function.return_failed_api(_(str(e)))
        return api_global_function.return_success_creation_api(product_product_obj.id, product_product_obj.id)
