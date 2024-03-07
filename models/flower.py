from odoo import models, fields


class Flower(models.Model):
    _name = 'flower'
    _description = 'Flower Shop'

    # Fields
    Common_name = fields.Char(string="Common Name")
    scientific_name = fields.Char(string="Scientific Name")
    season_start = fields.Date(string="Season Start")
    season_end = fields.Date(string="Season End")
    watering_frequency = fields.Integer(string="Watering Amount", help='Should be watered once every x days')
    watering_amount = fields.Float(string="Watering Amount", help='In milliliters')

    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.scientific_name, flower.Common_name)) for flower in self]

# class FlowerProduct(models.Model):
#     _inherit = 'product.template'
#
#     is_flower = fields.Boolean(string="Is Flower Product?")
#     flower_id = fields.Many2one('flower', string="Flower")
#     Watering_frequency = fields.Integer(string="Watering Frequency")
#
#     # class Product(models.Model):
#     #     _inherit = 'product.template'
#     #
#     #     is_flower = fields.Boolean(string="Is Flower Product?")
#     #     flower_id = fields.Many2one('flower', string="Flower")
#     # from odoo import models, fields
#     #
#     # class Flower(models.Model):
#     #     _name = 'flower'
#     #     _description = 'Flower Shop'
#     #
#     #     # Fields
#     #     common_name = fields.Char(string="Common Name")
#     #     season_start = fields.Date(string="Season Start")
#     #     season_end = fields.Date(string="Season End")
#     #     watering_amount = fields.Float(string="Watering Amount")
#     #     watering_frequency = fields.Integer(string="Watering Frequency")
