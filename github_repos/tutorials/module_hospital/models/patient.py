from datetime import date, datetime

from odoo import api, fields, models  # pyright: ignore[reportMissingImports]

from odoo.exceptions import UserError  # pyright: ignore[reportMissingImports]

class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #chatter
    _description = 'Hospital Patients'

    name = fields.Char(string='Name', tracking=True)
    blood_group = fields.Selection([
        ('a_positive', 'A+'),
        ('a_negative', 'A-'),
        ('b_positive', 'B+'),
        ('b_negative', 'B-'),
        ('ab_positive', 'AB+'),
        ('ab_negative', 'AB-'),
        ('o_positive', 'O+'),
        ('o_negative', 'O-'),
    ], string='Blood Group', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, copy=False)
    phone = fields.Char(string='Phone', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    medical_history = fields.Text(string='Medical History', tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    latest_appointment_id = fields.Many2one(
        'hospital.appointment',
        string='Latest Appointment',
        compute='_compute_latest_appointment_id',
    )
    emergency_contact_name = fields.Char(string='Guardian Name', tracking=True)
    emergency_contact_relationship = fields.Char(string='Relationship', tracking=True)
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone', tracking=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    consultation_fee = fields.Monetary(string='Consultation Fee', currency_field='currency_id', default=0.0)
    medicine_charges = fields.Monetary(string='Medicine Charges', currency_field='currency_id', default=0.0)
    tax_amount = fields.Monetary(string='Tax', currency_field='currency_id', default=0.0)
    discount_amount = fields.Monetary(string='Discount', currency_field='currency_id', default=0.0)
    grand_total = fields.Monetary(
        string='Grand Total',
        currency_field='currency_id',
        compute='_compute_grand_total',
        store=True,
    )
    active = fields.Boolean(string='Active', default=True, tracking=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            today = date.today()
            if record.date_of_birth:
                record.age = today.year - record.date_of_birth.year
            else:
                record.age = 0

    @api.depends('appointment_ids.appointment_date', 'appointment_ids.appointment_time')
    def _compute_latest_appointment_id(self):
        for record in self:
            if record.appointment_ids:
                record.latest_appointment_id = sorted(
                    record.appointment_ids,
                    key=lambda appointment: (
                        appointment.appointment_date or date.min,
                        appointment.appointment_time or datetime.min,
                        appointment.id,
                    ),
                )[-1]
            else:
                record.latest_appointment_id = False

    @api.depends('consultation_fee', 'medicine_charges', 'tax_amount', 'discount_amount')
    def _compute_grand_total(self):
        for record in self:
            record.grand_total = (
                (record.consultation_fee or 0.0)
                + (record.medicine_charges or 0.0)
                + (record.tax_amount or 0.0)
                - (record.discount_amount or 0.0)
            )
    
    def object_View_appointment(self):
        return {
            'effect' : {
                'fadeout': 'slow',
                'message': 'success',
                'type' : 'rainbow_man',
            }
        }
    
    @api.model
    def create(self,vals):
        patient = super().create(vals) #create method is used to create a new record in the database. It takes a dictionary of field values as an argument and returns the newly created record.

        partner = self.env['res.partner'].create({
            "name" : patient.name,
            "email": patient.email,
            "phone": patient.phone,
        })

        patient.partner_id = partner.id
        return patient
    
    #excel sheet
    def action_print_excel(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "url": "/patient/excel/%s" % self.id,
            "target": "self",
        }