from odoo import fields, models  # pyright: ignore[reportMissingImports]

class HospitalDoctors(models.Model):
    _name = 'hospital.doctors'
    _description = 'Hospital Doctors'

    name = fields.Char(string='Doctor Name', required=True, tracking=True)
    department = fields.Char(string='Department', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    license_number = fields.Char(string='License Number', tracking=True)
    notes = fields.Text(string='Notes')


