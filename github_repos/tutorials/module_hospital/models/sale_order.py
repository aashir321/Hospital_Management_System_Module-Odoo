from odoo import api, fields, models  # pyright: ignore[reportMissingImports]

class sale_order(models.Model):
    _inherit = 'sale.order'

    partner_tags = fields.Many2many(
    'res.partner.category', 
    string="Customer Tags", 
    related='partner_id.category_id')
    reference = fields.Char(string="Reference", copy=False, readonly=True, default="new")




    @api.model
    def create(self, vals):
        if vals.get("reference", "New") == "New":
            vals["reference"] = self.env["ir.sequence"].next_by_code("sale.reference.sequence")
        return super().create(vals)