from odoo import api, fields, models, _, SUPERUSER_ID, tools
import logging
from . import api_global_function

_logger = logging.getLogger(__name__)
DATES_FORMAT = "%Y-%m-%d"


class res_partner(models.Model):
    _inherit = "res.partner"

    come_from = fields.Char('Come From')

    @api.model
    def get_partner_info(self, **args):
        lang = args.get('lang')
        if lang == 'ar':
            lang = 'ar_SY'
        elif lang == 'en':
            lang = 'en_US'
        else:
            return api_global_function.return_failed_request_vals("Wrong Language Name", "عفوا اللغه غير مدعومه")
        domain = []
        if args.get("customer_id", False):
            domain.append(('id', '=', args.get("customer_id", False)))
        res_partner_objs = self.env['res.partner'].sudo().search(domain)
        result = []
        for res_partner_obj in res_partner_objs:
            result.append({
                'id': res_partner_obj.id,
                'name': res_partner_obj.name or '',
                'fullname': res_partner_obj.display_name or '',
                'phone': res_partner_obj.phone or '',
                'mobile': res_partner_obj.mobile or '',
                'email': res_partner_obj.email or '',
                'street': res_partner_obj.street or '',
                'street': res_partner_obj.street2 or '',
                'city': res_partner_obj.city or '',
                'state_name': res_partner_obj.state_id.name or '',
                'zip': res_partner_obj.zip or '',
                'country_id': res_partner_obj.country_id.name or '',
                'come_from':res_partner_obj.come_from or 'Odoo',
            })
        return api_global_function.return_success_list_api(result)

    def check_partner_vals(self, args):
        partner_vals = {}
        if args.get("RequestID", False):
            partner_vals.update({'id': args.get("RequestID", False)})
        try:
            if not args.get('name', False):
                return False, api_global_function.return_failed_request_vals("Customer Name Not provided",
                                                                             "عفوا اسم العميل مش موجود")
            partner_vals.update({'name': args.get('name', False)})
            if not args.get('come_from', False):
                return False, api_global_function.return_failed_request_vals("Come From Not provided",
                                                                             "عفوا المصدر مش موجود")
            partner_vals.update({'come_from': args.get('come_from', False)})
            if not args.get('mobile', False):
                return False, api_global_function.return_failed_request_vals("Customer Mobile Not provided",
                                                                             "عفوا رقم الجوال مش موجود")
            partner_vals.update({'mobile': args.get('mobile', False)})
            if not args.get('email', False):
                return False, api_global_function.return_failed_request_vals("Customer Email Not provided",
                                                                             "عفوا البريد الالكترونى مش موجود")
            partner_vals.update({'email': args.get('email', False)})
            if args.get('phone', False):
                partner_vals.update({'phone': args.get('phone', False)})
        except Exception as e:
            arabic_message = "%s  " % _(str(e)),
            englishmessage = "%s." % _(str(e))
            return False, api_global_function.return_failed_request_vals(englishmessage, arabic_message)
        return True, partner_vals

    def add_partner(self, **args):
        request_id = args.get("RequestID", False)
        check_vals, partner_vals = self.check_partner_vals(args)
        if not check_vals:
            return partner_vals
        try:
            if not request_id:
                res_partner_obj = self.with_user(args.get('userId')).sudo().create(partner_vals)
            else:
                #Update Request ID
                res_partner_obj = self.with_user(args.get('userId')).sudo().browse(request_id)
                res_partner_obj.with_user(args.get('userId')).sudo().write(partner_vals)
        except Exception as e:
            self.env.cr.rollback()
            return api_global_function.return_failed_api(_(str(e)))
        if not request_id:
            return api_global_function.return_success_creation_api(res_partner_obj.id, res_partner_obj.id)
        else:
            return api_global_function.return_success_update_api(res_partner_obj.id, res_partner_obj.id)
