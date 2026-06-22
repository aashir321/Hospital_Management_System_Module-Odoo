from odoo import api, fields, models

class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    _description = 'Hospital Patients'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    medical_history = fields.Text(string='Medical History')
