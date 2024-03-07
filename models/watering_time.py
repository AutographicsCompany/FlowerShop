from odoo import models, fields


class WateringTime(models.Model):
    _name = "flower.water"
    _description = "Flower Watering"
    _order = "date"

    serial_id = fields.Many2one("stock.lot")
    date = fields.Date(string="Date")
    product_id = fields.Many2one("product.product", related="serial_id.product_id", store=True)
    is_flower = fields.Boolean(related='product_id.is_flower', string="Is Flower Product", store=True)
