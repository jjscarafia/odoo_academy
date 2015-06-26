# -*- coding utf -8 -*-
from openerp import fields, models


class Partner(models.Model):

    """docstring for Parner"""
    _inherit = 'res.partner'

    instructor = fields.Boolean(
        "Instructor",
        default=True,
    )
    attendee = fields.Boolean(string="Is attendee?")
    session_fields_ids = fields.Many2many(
        'openacademy.sessions',
        string="Asiste a la sesion", readonly=True,
    )
