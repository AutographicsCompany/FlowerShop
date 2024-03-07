from odoo import models, fields, api, _
import requests


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    weather_api_key = fields.Char(string='Weather API Key')
    contact_id = fields.Many2one('res.partner', string='Contact', required=True)  # Ensure contact is required
    weather_data_ids = fields.One2many('stock.warehouse.weather', 'warehouse_id', string='Weather Data')


    def _get_api_key_and_location(self):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")
        if not api_key or api_key == "unset":
            raise ValueError("Weather API key is not set")

        if not self.contact_id or not self.contact_id.partner_latitude or not self.contact_id.partner_longitude:
            raise ValueError(
                "Warehouse location is not set. Please ensure the contact has valid latitude and longitude.")

        return api_key, self.contact_id.partner_latitude, self.contact_id.partner_longitude

    def get_weather(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location()
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()
            self.env["stock.warehouse.weather"].create({
                "warehouse_id": self.id,
                "description": entries["weather"][0]["description"],
                "pressure": entries["main"]["pressure"],
                "temperature": entries["main"]["temp"],
                "humidity": entries["main"]["humidity"] / 100,
                "wind_speed": entries["wind"]["speed"],
                "rain_volume": entries["rain"]["1h"] if "rain" in entries else 0,
                "capture_time": fields.Datetime.now(),
            })
        except Exception as e:
            if show_error:
                raise ValueError(f"Failed to fetch weather data: {str(e)}")

    def action_button_fetch_weather(self):
        self.get_weather(show_error=True)

    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)

    def get_forecast_all_warehouses(self, show_error=True):
        flower_serials_to_water = self.env["stock.production.lot"]
        for warehouse in self:
            api_key, lat, lng = warehouse._get_api_key_and_location()
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={api_key}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                entries = response.json()
                is_rainy_today = False
                for i in range(0, 8):  # Check for 24 hours forecast (8 entries, 3-hour intervals)
                    if "rain" in entries["list"][i]:
                        rain = entries["list"][i]["rain"]["3h"]
                        if rain > 0.2:
                            is_rainy_today = True
                            break
                if is_rainy_today:
                    flower_products = self.env["product.product"].search([("is_flower", "=", True)])
                    quants = self.env["stock.quant"].search([
                        ("product_id", "in", flower_products.ids),
                        ("location_id", "=", warehouse.lot_stock_id.id)
                    ])
                    flower_serials_to_water |= quants.lot_id
            except Exception as e:
                if show_error:
                    raise ValueError(f"Failed to fetch forecast data: {str(e)}")
        for flower_serial in flower_serials_to_water:
            self.env["flower.water"].create({
                "serial_id": flower_serial.id,
            })
