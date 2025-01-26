# -*- coding: utf-8 -*-
""" Odoo Rest Api Integration"""

import re
import binascii, hashlib
import random
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, except_orm

import logging
LOGGER = logging.getLogger(__name__)


class User(models.Model):
    """
    """
    _inherit = 'res.users'

    def _get_random_secret_key(self):
        return str(random.randint(1000, 9999))

    api_access_token = fields.Char()
    secret_key = fields.Char(required=False, default=_get_random_secret_key)
    encrypted_secret_key = fields.Char(required=False)
    otp = fields.Char()
    otp_valid_date = fields.Datetime("OTP Valid Date")
    number_of_otp_try = fields.Integer("Number of OTP",default=0)
    block_send_otp_till = fields.Datetime("Block Send OTP Till")

    _sql_constraints = [("unique_api_access_token",
                         "UNIQUE(api_access_token)",
                         _('API Access Token should be unique')),
                        ("unique_encrypted_secret_key",
                         "UNIQUE(encrypted_secret_key)",
                         _('User secret key should be unique'))]

    @api.model
    def num_ar_cnv(self, num):
        ar = u'٠١٢٣٤٥٦٧٨٩'
        en = u'0123456789'
        ret = ''
        for n in num:
            n2 = n if not n in en else ar[int(n)]
            ret += n2
        return ret

    @api.onchange('secret_key')
    def _onchange_secret_key(self):
        self.api_access_token = False

    @api.onchange('login')
    def _onchange_login(self):
        self.api_access_token = False

    def _generate_encrypted_secret_key(self):
        self.ensure_one()
        secret_key = self.secret_key or str(random.randint(1000, 9999))
        h = hashlib.new('sha256', secret_key.encode('utf-8'))
        self.encrypted_secret_key = h.hexdigest()
        return self.encrypted_secret_key

    def _generate_api_access_token(self):
        self.ensure_one()
        dk = hashlib.pbkdf2_hmac('sha256', self.secret_key.encode('utf-8'), self.login.encode('utf-8'), 100000)
        token = binascii.hexlify(dk).decode('utf-8')
        self.api_access_token = token
        return token
