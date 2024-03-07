from odoo import models, fields


class WarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Warehouse Weather'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    temperature = fields.Float(string='Temperature')
    pressure = fields.Float(string='Pressure')
    humidity = fields.Float(string='Humidity')
    wind_speed = fields.Float(string='Wind Speed')
    rain_volume = fields.Float(string='Rain Volume (mm)')
    description = fields.Char(string='Description')
    capture_time = fields.Datetime(string='Capture Time', default=fields.Datetime.now)
