from odoo import api, fields, models  # pyright: ignore[reportMissingImports]

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointments'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patients', string='Patient')
    appointment_date = fields.Date(string='Appointment Date', default=fields.Date.context_today, tracking=True)
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now, tracking=True)
    Booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today, tracking=True)
    doctor_id = fields.Many2one('hospital.doctors', string='Doctor', tracking=True)
    department = fields.Char(related='doctor_id.department', string='Department', store=True, readonly=False)
    email = fields.Char(string = 'Email')
    symptoms = fields.Text(string='Symptoms', tracking=True)
    diagnosis = fields.Text(string='Diagnosis', tracking=True)
    prescription = fields.Html(string = 'Prescription')
    doctor_notes = fields.Text(string='Doctor Notes', tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priority', default='0', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')], string='Status', default='draft',required=True, tracking=True)


    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.email = self.patient_id.email