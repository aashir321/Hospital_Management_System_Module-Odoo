from odoo import api ,fields, models # pyright: ignore[reportMissingImports]

class AccountMove(models.Model):
    _inherit = "account.move"

    sale_reference = fields.Char(
        string="Reference"
    )
