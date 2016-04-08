# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date, time
from openerp import models, fields, api, exceptions


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(
        "Titulo",
        required=True,
    )
    hours = fields.Integer(
        string="Horas catedras",
        help='Ingrese solo números',
    )
    responsible_id = fields.Many2one(
        'res.users',
        ondelete="set null",
        string="Profesor",
        index=True,
    )
    session_ids = fields.One2many(
        'openacademy.sessions',
        'course_id',
        string="Sesiones",
        required=True,
    )


class Session_fields(models.Model):

    """"""

    _name = 'openacademy.session_fields'

    name = fields.Char(string="Nombre")


class Sessions(models.Model):
    _name = 'openacademy.sessions'

    session_fields_id = fields.Many2one(
        'openacademy.session_fields',
        string="Session",
    )
    start_date = fields.Date(
        "Fecha de inicio",
        default=fields.Date.today,
    )
    duration = fields.Float(
        "Duracion",
        digits=(6, 2),
        help="Días de dictado",
    )
    seats = fields.Integer(
        string="Numero de asientos",
    )
    active = fields.Boolean(
        default=True,
    )
    instructor_id = fields.Many2one(
        'res.partner',
        string="Instructor",
        domain=['|', ('instructor', '=', True),
                ('category_id.name', 'ilike', "teacher")],
    )
    course_id = fields.Many2one(
        'openacademy.course',
        ondelete='cascade',
        string="Curso",
        required=True,
    )
    attendee_ids = fields.Many2many(
        'res.partner',
        string="Alumnos",
    )
    difference = fields.Integer(
        string='Termina en (Días)',
        compute='_difference',
    )
    end_date = fields.Date(
        string="End Date",
        store=True,
        compute='_get_end_date',
        inverse='_set_end_date',
    )
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours',
                         inverse='_set_hours',
                         )

    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_instructor(self):
        """
        """
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError(
                "El Intructor de la sesion no puede ser un alumno")
        if self.seats < 0 or self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title':
                        "Aviso!",
                    'message':
                        "El número de asientos es menor al número de Alumnos",
                },
            }

    @api.one
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        """
            add duration to start_date, but: monday + 5 days = Saturday, so
            subtract one second to get on Friday instead
        """
        if not (self.start_date and self.duration):
            self.end_date = self.start_date
            return

        start = fields.Datetime.from_string(self.start_date)
        duration = timedelta(days=self.duration, seconds=-1)
        self.end_date = start + duration

    @api.one
    def _set_end_date(self):
        """
        """
        if not (self.start_date and self.end_date):
            return
        start_date = fields.Datetime.from_string(self.start_date)
        end_date = fields.Datetime.from_string(self.end_date)

        self.duration = (end_date - start_date).days + 1

    @api.one
    @api.depends('end_date',)
    def _difference(self):
        """
        Calculate the difference in days remaining to complete the course
        """
        today = datetime.now()
        end = fields.Datetime.from_string(self.end_date)
        self.difference = (end - today).days + 1

    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24

    @api.one
    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)

    @api.one
    @api.constrains('seats', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        """
            Check that the instructor is not a an assistant
        """
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError(
                "El Intructor de la sesion no puede ser un alumno")

        if self.seats < 0 or self.seats < len(self.attendee_ids):
            raise exceptions.ValidationError(
                "El valor de los asientos es menor al número de Alumnos")
