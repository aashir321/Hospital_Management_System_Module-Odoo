from odoo import api, fields, models  # pyright: ignore[reportMissingImports]

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointments'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patients', string='Patient')
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now, tracking=True)
    Booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today, tracking=True)
    email = fields.Char(string = 'Email')
    prescription = fields.Html(string = 'Prescription')


    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.email = self.patient_id.email