import json
from datetime import date

from root import enums
from root.handlers import BaseHandler


class TimeSlotHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        data = {
            1: {'id': 1, 'adspot_id': 1, 'from_time': '00:00', 'to_time': '01:00'},
            2: {'id': 2, 'adspot_id': 0, 'from_time': '01:00', 'to_time': '02:00'},
            3: {'id': 3, 'adspot_id': 0, 'from_time': '02:00', 'to_time': '03:00'},
            4: {'id': 4, 'adspot_id': 2, 'from_time': '03:00', 'to_time': '04:00'},
            5: {'id': 5, 'adspot_id': 0, 'from_time': '04:00', 'to_time': '05:00'},
            6: {'id': 6, 'adspot_id': 3, 'from_time': '05:00', 'to_time': '06:00'},
            7: {'id': 7, 'adspot_id': 0, 'from_time': '06:00', 'to_time': '07:00'},
            8: {'id': 8, 'adspot_id': 0, 'from_time': '07:00', 'to_time': '08:00'},
            9: {'id': 9, 'adspot_id': 1, 'from_time': '08:00', 'to_time': '09:00'},
            10: {'id': 10, 'adspot_id': 0, 'from_time': '09:00', 'to_time': '10:00'},
            11: {'id': 11, 'adspot_id': 0, 'from_time': '10:00', 'to_time': '11:00'},
            12: {'id': 12, 'adspot_id': 0, 'from_time': '11:00', 'to_time': '12:00'},
            13: {'id': 13, 'adspot_id': 1, 'from_time': '12:00', 'to_time': '13:00'},
            14: {'id': 14, 'adspot_id': 1, 'from_time': '13:00', 'to_time': '14:00'},
            15: {'id': 15, 'adspot_id': 2, 'from_time': '14:00', 'to_time': '15:00'},
            16: {'id': 16, 'adspot_id': 1, 'from_time': '15:00', 'to_time': '16:00'},
            17: {'id': 17, 'adspot_id': 4, 'from_time': '16:00', 'to_time': '17:00'},
            18: {'id': 18, 'adspot_id': 1, 'from_time': '17:00', 'to_time': '18:00'},
            19: {'id': 19, 'adspot_id': 0, 'from_time': '18:00', 'to_time': '19:00'},
            20: {'id': 20, 'adspot_id': 0, 'from_time': '19:00', 'to_time': '20:00'},
            21: {'id': 21, 'adspot_id': 0, 'from_time': '20:00', 'to_time': '21:00'},
            22: {'id': 22, 'adspot_id': 5, 'from_time': '21:00', 'to_time': '22:00'},
            23: {'id': 23, 'adspot_id': 0, 'from_time': '22:00', 'to_time': '23:00'},
            24: {'id': 24, 'adspot_id': 6, 'from_time': '23:00', 'to_time': '24:00'},

        }
        r = json.dumps(data)
        self.write(r)
