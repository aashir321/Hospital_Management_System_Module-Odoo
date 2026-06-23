from odoo import api, fields, models  # pyright: ignore[reportMissingImports]
from datetime import date


class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patients'

    name = fields.Char(string='Name', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    medical_history = fields.Text(string='Medical History', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            today = date.today()
            if record.date_of_birth:
                record.age = today.year - record.date_of_birth.year
            else:
                record.age = 0