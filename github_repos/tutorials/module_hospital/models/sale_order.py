from odoo import api, fields, models  # pyright: ignore[reportMissingImports]
from odoo.exceptions import UserError #pyright: ignore[reportMissingImports]
class sale_order(models.Model):
    _inherit = 'sale.order'

    partner_tags = fields.Many2many(
    'res.partner.category', 
    string="Customer Tags", 
    related='partner_id.category_id')
    reference = fields.Char(string="Reference", copy=False, readonly=True, default="New")
    approval_state = fields.Selection([
        ("draft", "Draft"),
        ("waiting", "Waiting for Approval"),
        ("approved", "Approved"),
    ], default="draft", tracking=True)
    approved_by = fields.Many2one(
        "res.users",
        string="Approved By",
        readonly=True,
        )
    approval_date = fields.Datetime(
        readonly=True
        )
    

    def action_send_for_approval(self):
        if self.env.user.has_group("module_hospital.group_sale_order_approver"):
            raise UserError("Approver cannot send quotation for approval.")

        self.ensure_one()

        if self.approval_state != "draft":
            raise UserError("Quotation is not in draft state.")

        self.approval_state = "waiting"

        # Approver Group
        approver_group = self.env.ref("module_hospital.group_sale_order_approver")

        # Activity Type (To Do)
        activity_type = self.env.ref("mail.mail_activity_data_todo")

        # Create Activity for every Approver
        for user in approver_group.users:
            self.env["mail.activity"].create({
                "activity_type_id": activity_type.id,
                "summary": "Request for Approval",
                "note": f"{self.env.user.name} requested approval for quotation {self.name}.",
                "user_id": user.id,
                "res_id": self.id,
                "res_model_id": self.env["ir.model"]._get_id("sale.order"),
                "date_deadline": fields.Date.today(),
            })

    def action_approve_order(self):
        self.ensure_one()
        if self.approval_state != "waiting":
            raise UserError("Quotation is not waiting for approval.")

        if not self.env.user.has_group("module_hospital.group_sale_order_approver"):
            raise UserError("You are not allowed to approve this quotation.")

        self.approval_state = "approved"
        self.approved_by = self.env.user
        self.approval_date = fields.Datetime.now()

        self.message_post(
            body=f"{self.env.user.name} approved this quotation."
        )

    def action_confirm(self):
        for order in self:
            if (
                not self.env.user.has_group("module_hospital.group_sale_order_approver")
                and order.approval_state != "approved"
            ):
                raise UserError("Quotation is not approved.")

        res = super().action_confirm()

        for order in self:
            order.message_post(
                body=f"Quotation confirmed by <b>{self.env.user.name}</b>."
            )

        return res
    

    @api.model
    def create(self, vals):
        if vals.get("reference", "New") == "New":
            vals["reference"] = self.env["ir.sequence"].next_by_code(
                "sale.reference.sequence"
            )

        order = super().create(vals)

        # Approver creates quotation
        if self.env.user.has_group("module_hospital.group_sale_order_approver"):
            order.write({
                "approval_state": "approved",
                "approved_by": self.env.user.id,
                "approval_date": fields.Datetime.now(),
            })

        order.message_post(
            body=f"{self.env.user.name} created this quotation."
        )

        return order