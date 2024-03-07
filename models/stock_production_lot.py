from odoo import models, fields, api
from datetime import date, datetime, timedelta


class StockProductionLot(models.Model):
    _inherit = "stock.lot"
    water_ids = fields.One2many("flower.water", "serial_id")
    is_flower = fields.Boolean(related='product_id.is_flower', string="Is Flower Product", store=True)

    def action_water_flower(self):
        flowers = self.filtered(lambda rec: rec.is_flower)
        for record in flowers:
            if record.water_ids:
                last_watered_date = record.water_ids[0].date
                frequency = record.product_id.flower_id.watering_frequency
                today = datetime.now().date()

                if not last_watered_date or not isinstance(frequency, int):
                    continue

                days_since_last_watering = (today - last_watered_date).days

                if days_since_last_watering >= frequency:
                    self.env["flower.water"].create({
                        "serial_id": record.id,
                    })

            print(record.id)
