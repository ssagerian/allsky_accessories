import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class SensorData:
    HS_TIME_STAMP_KEY = 'HS_TIME_STAMP'
    HS_TEMPERATURE_KEY = 'HS_TEMPERATURE'
    HS_HUMIDITY_KEY = 'HS_HUMIDITY'
    HS_DEW_HEATER_KEY = 'HS_DEW_HEATER_STATUS'
    HS_FAN_STATUS_KEY = 'HS_FAN_STATUS'

    def __init__(self, temperature=None, humidity=None, dew_heater_status=None, fan_status=None, default_expire=60):
        self.data_dict = {
            self.HS_TIME_STAMP_KEY: {'value': datetime.now(), 'expires': default_expire},
            self.HS_TEMPERATURE_KEY: {'value': temperature, 'expires': default_expire},
            self.HS_HUMIDITY_KEY: {'value': humidity, 'expires': default_expire},
            self.HS_DEW_HEATER_KEY: {'value': dew_heater_status, 'expires': default_expire},
            self.HS_FAN_STATUS_KEY: {'value': fan_status, 'expires': default_expire}
        }

    def get_data_json(self):
        return json.dumps(self.data_dict, indent=2, cls=DateTimeEncoder)

    def save_to_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.data_dict, json_file, indent=4, cls=DateTimeEncoder)

