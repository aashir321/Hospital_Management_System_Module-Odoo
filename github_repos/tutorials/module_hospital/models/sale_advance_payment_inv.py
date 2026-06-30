from odoo import fields, models, api # pyright: ignore[reportMissingImports]

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    reference = fields.Char(string="Reference")


    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_id = self.env.context.get("active_id")

        if active_id:
            sale_order = self.env["sale.order"].browse(active_id)
            res["reference"] = sale_order.reference

        return res