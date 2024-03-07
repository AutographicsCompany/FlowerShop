from odoo import models, fields


class FlowerProduct(models.Model):
    _inherit = 'product.template'

    is_flower = fields.Boolean(string="Is Flower Product?")
    flower_id = fields.Many2one('flower', string="Flower")


