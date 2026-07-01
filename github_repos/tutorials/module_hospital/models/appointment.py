from odoo import api, fields, models  # pyright: ignore[reportMissingImports]
from odoo.exceptions import UserError #pyright: ignore[reportMissingImports]


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
    line_ids = fields.One2many("hospital.appointment.line",
                                 "appointment_id", #many2one field in appointment_line.py this will automatically connect this one2many with many2one
                                 string="Services")
    grand_total = fields.Float(string="Grand Total",
                               compute="_compute_grand_total",
                               store=True)
    invoice_count = fields.Integer(
        compute="_compute_invoice_count",
    )
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

    @api.depends("line_ids.subtotal")
    def _compute_grand_total(self):
        for appointment in self:
            appointment.grand_total = sum(
                appointment.line_ids.mapped('subtotal') #mapped is used to get the value of a field from a recordset. It returns a list of values for the specified field from all records in the recordset.
            )
    
    def action_create_invoice(self):
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.patient_id.partner_id.id,
            "invoice_date": fields.Date.context_today(self),
            "sale_reference": f"APT-{self.id}",
            "payment_reference": f"APT-{self.id}",
        })

        for line in self.line_ids:
            self.env["account.move.line"].create({
                "move_id": invoice.id,
                "product_id": line.product_id.id,
                "quantity": line.quantity,
                "price_unit": line.price_unit,
                "name": line.product_id.name,
            })

        return {
            "type": "ir.actions.act_window",
            "name": "Customer Invoice",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id,
            "target": "current",
        }

    @api.depends("patient_id.partner_id")
    def _compute_invoice_count(self):
        for record in self:
            if record.patient_id.partner_id:
                record.invoice_count = self.env["account.move"].search_count([
                ("partner_id", "=", record.patient_id.partner_id.id),
                ("move_type", "=", "out_invoice"),
            ])
            else:
                record.invoice_count = 0
    
    def action_view_patient_invoices(self):
        self.ensure_one()

        action = self.env.ref("account.action_move_out_invoice_type").read()[0]

        action["name"] = "Patient Invoices"
        action["domain"] = [
            ("partner_id", "=", self.patient_id.partner_id.id),
            ("move_type", "=", "out_invoice"),
        ]
        action["context"] = {
            "default_partner_id": self.patient_id.partner_id.id,
            "default_move_type": "out_invoice",
        }

        return action
