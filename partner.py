# -*- coding utf -8 -*-
from openerp import fields, models


class Partner(models.Model):

    """docstring for Parner"""
    _inherit = 'res.partner'

    instructor = fields.Boolean(
        "Instructor",
        default=False,
    )
    session_ids = fields.Many2many(
        'openacademy.session',
        string="Asiste a la sesion", readonly=True,
    )
