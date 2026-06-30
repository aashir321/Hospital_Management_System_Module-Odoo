from odoo import fields, models ,api # pyright: ignore[reportMissingImports]

class HospitalAppointmentLine(models.Model):
    _name = "hospital.appointment.line"
    _description = "Services"

    appointment_id = fields.Many2one(
        "hospital.appointment",
        string="Appointment",
        ondelete="cascade",
        required=True,
    )

    product_id = fields.Many2one(
        "product.product",
        string="Service",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity",
        default=1.0,
    )

    price_unit = fields.Float(
        string="Unit Price"
    )

    subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_subtotal",
        store=True,
    )


    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
        else :
            self.price_unit = 0.0
    

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit