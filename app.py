import os
import sqlite3
import requests
import logging

import self
from flask import Flask, render_template, request, jsonify
from datetime import datetime


class RoundaboutTrafficApp:
    NAIROBI_ROAD_POINTS = {
        'haile-selassie': [
            {
                'name': 'Haile Selassie towards Upperhill',
                'latitude': -1.2833,
                'longitude': 36.8158,
                'bearing': 0
            },
            {
                'name': 'Haile Selassie towards Nairobi Hospital',
                'latitude': -1.2835,
                'longitude': 36.8159,
                'bearing': 180
            },
            {
                'name': 'Haile Selassie towards University Way',
                'latitude': -1.2834,
                'longitude': 36.8160,
                'bearing': 90
            },
            {
                'name': 'Haile Selassie towards Central Police Station',
                'latitude': -1.2832,
                'longitude': 36.8157,
                'bearing': 270
            }
        ],
        'uhuru-highway': [
            {
                'name': 'Uhuru Highway towards National Archives',
                'latitude': -1.2841,
                'longitude': 36.8222,
                'bearing': 0
            },
            {
                'name': 'Uhuru Highway towards Nairobi Museum',
                'latitude': -1.2839,
                'longitude': 36.8223,
                'bearing': 180
            },
            {
                'name': 'Uhuru Highway towards KICC',
                'latitude': -1.2842,
                'longitude': 36.8225,
                'bearing': 90
            },
            {
                'name': 'Uhuru Highway towards City Center',
                'latitude': -1.2840,
                'longitude': 36.8219,
                'bearing': 270
            }
        ],
        'kenyatta-avenue': [
            {
                'name': 'Kenyatta Avenue towards City Hall',
                'latitude': -1.2820,
                'longitude': 36.8120,
                'bearing': 0
            },
            {
                'name': 'Kenyatta Avenue towards Supreme Court',
                'latitude': -1.2822,
                'longitude': 36.8122,
                'bearing': 180
            },
            {
                'name': 'Kenyatta Avenue towards Parliament Road',
                'latitude': -1.2821,
                'longitude': 36.8121,
                'bearing': 90
            },
            {
                'name': 'Kenyatta Avenue towards High Court',
                'latitude': -1.2819,
                'longitude': 36.8123,
                'bearing': 270
            }
        ],
        'ngong-road': [
            {
                'name': 'Ngong Road towards Yaya Centre',
                'latitude': -1.2998,
                'longitude': 36.7783,
                'bearing': 0
            },
            {
                'name': 'Ngong Road towards ABC Place',
                'latitude': -1.3005,
                'longitude': 36.7790,
                'bearing': 180
            },
            {
                'name': 'Ngong Road towards Strathmore University',
                'latitude': -1.3000,
                'longitude': 36.7785,
                'bearing': 90
            },
            {
                'name': 'Ngong Road towards Prestige Plaza',
                'latitude': -1.2995,
                'longitude': 36.7778,
                'bearing': 270
            }
        ],
        'mombasa-road': [
            {
                'name': 'Mombasa Road towards JKIA',
                'latitude': -1.3192,
                'longitude': 36.8732,
                'bearing': 0
            },
            {
                'name': 'Mombasa Road towards City Cabanas',
                'latitude': -1.3200,
                'longitude': 36.8740,
                'bearing': 180
            },
            {
                'name': 'Mombasa Road towards Export Processing Zone',
                'latitude': -1.3195,
                'longitude': 36.8735,
                'bearing': 90
            },
            {
                'name': 'Mombasa Road towards Syokimau',
                'latitude': -1.3188,
                'longitude': 36.8728,
                'bearing': 270
            }
        ],
        'waiyaki-way': [
            {
                'name': 'Waiyaki Way towards Westlands',
                'latitude': -1.2649,
                'longitude': 36.7972,
                'bearing': 0
            },
            {
                'name': 'Waiyaki Way towards ABC Place',
                'latitude': -1.2655,
                'longitude': 36.7980,
                'bearing': 180
            },
            {
                'name': 'Waiyaki Way towards Safaricom House',
                'latitude': -1.2652,
                'longitude': 36.7975,
                'bearing': 90
            },
            {
                'name': 'Waiyaki Way towards Mountain View',
                'latitude': -1.2646,
                'longitude': 36.7968,
                'bearing': 270
            }
        ],
        'thika-road': [
            {
                'name': 'Thika Road towards Garden City Mall',
                'latitude': -1.2266,
                'longitude': 36.8687,
                'bearing': 0
            },
            {
                'name': 'Thika Road towards Roysambu',
                'latitude': -1.2272,
                'longitude': 36.8693,
                'bearing': 180
            },
            {
                'name': 'Thika Road towards Kasarani',
                'latitude': -1.2269,
                'longitude': 36.8690,
                'bearing': 90
            },
            {
                'name': 'Thika Road towards Githurai',
                'latitude': -1.2263,
                'longitude': 36.8684,
                'bearing': 270
            }
        ],
        'jogoo-road': [
            {
                'name': 'Jogoo Road towards Dandora',
                'latitude': -1.2820,
                'longitude': 36.8920,
                'bearing': 0
            },
            {
                'name': 'Jogoo Road towards Savannah',
                'latitude': -1.2826,
                'longitude': 36.8926,
                'bearing': 180
            },
            {
                'name': 'Jogoo Road towards Lucky Summer',
                'latitude': -1.2823,
                'longitude': 36.8923,
                'bearing': 90
            },
            {
                'name': 'Jogoo Road towards Eastleigh',
                'latitude': -1.2817,
                'longitude': 36.8917,
                'bearing': 270
            }
        ],
        'langata-road': [
            {
                'name': 'Langata Road towards Wilson Airport',
                'latitude': -1.3172,
                'longitude': 36.7920,
                'bearing': 0
            },
            {
                'name': 'Langata Road towards Nyayo Stadium',
                'latitude': -1.3178,
                'longitude': 36.7926,
                'bearing': 180
            },
            {
                'name': 'Langata Road towards Kenyatta National Hospital',
                'latitude': -1.3175,
                'longitude': 36.7923,
                'bearing': 90
            },
            {
                'name': 'Langata Road towards Karen',
                'latitude': -1.3169,
                'longitude': 36.7917,
                'bearing': 270
            }
        ],
        'mbagathi-way': [
            {
                'name': 'Mbagathi Way towards Nairobi West',
                'latitude': -1.3050,
                'longitude': 36.7850,
                'bearing': 0
            },
            {
                'name': 'Mbagathi Way towards Industrial Area',
                'latitude': -1.3056,
                'longitude': 36.7856,
                'bearing': 180
            },
            {
                'name': 'Mbagathi Way towards Kibera',
                'latitude': -1.3053,
                'longitude': 36.7853,
                'bearing': 90
            },
            {
                'name': 'Mbagathi Way towards Carnivore Restaurant',
                'latitude': -1.3047,
                'longitude': 36.7847,
                'bearing': 270
            }
        ],
        'ralph-bunche-road': [
            {
                'name': 'Ralph Bunche Road towards UN Headquarters',
                'latitude': -1.2755,
                'longitude': 36.8193,
                'bearing': 0
            },
            {
                'name': 'Ralph Bunche Road towards Central Bank',
                'latitude': -1.2761,
                'longitude': 36.8199,
                'bearing': 180
            },
            {
                'name': 'Ralph Bunche Road towards Hurlingham',
                'latitude': -1.2758,
                'longitude': 36.8196,
                'bearing': 90
            },
            {
                'name': 'Ralph Bunche Road towards Upper Hill',
                'latitude': -1.2752,
                'longitude': 36.8190,
                'bearing': 270
            }
        ]
    }


    def __init__(self, tomtom_api_key):
        self.app = Flask(__name__)
        self.tomtom_api_key = tomtom_api_key
        self.db_path = 'traffic_requests.db'

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.setup_database()
        self.setup_routes()

    def get_road_traffic_data(self, road_points):
        road_traffic_data = []

        for road in road_points:
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={self.tomtom_api_key}&point={road['latitude']},{road['longitude']}&heading={road['bearing']}"

            try:
                response = requests.get(url, timeout=10)
                data = response.json()

                traffic_info = {
                    'name': road['name'],
                    'latitude': road['latitude'],
                    'longitude': road['longitude'],
                    'currentSpeed': round(data.get('flowSegmentData', {}).get('currentSpeed', 0), 2),
                    'freeFlowSpeed': round(data.get('flowSegmentData', {}).get('freeFlowSpeed', 0), 2),
                    'congestionLevel': self._calculate_congestion_level(
                        data.get('flowSegmentData', {}).get('currentSpeed', 0),
                        data.get('flowSegmentData', {}).get('freeFlowSpeed', 0)
                    )
                }
                road_traffic_data.append(traffic_info)
                self._log_request(road['name'])
            except Exception as e:
                self.logger.error(f"Traffic data error for {road['name']}: {e}")
                road_traffic_data.append({
                    'name': road['name'],
                    'error': str(e)
                })

        return road_traffic_data

    def _calculate_congestion_level(self, current_speed, free_flow_speed):
        if current_speed == 0 or free_flow_speed == 0:
            return 'Blocked'

        speed_ratio = current_speed / free_flow_speed
        if speed_ratio > 0.8:
            return 'Low'
        elif speed_ratio > 0.5:
            return 'Medium'
        else:
            return 'High'

    def _log_request(self, location):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO requests (location, timestamp) 
                    VALUES (?, datetime('now'))
                ''', (location,))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Request logging error: {e}")

    def setup_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            self.logger.error(f"Database setup error: {e}")

    def setup_routes(self):
        @self.app.route('/', methods=['GET'])
        def index():
            return render_template('index.html', road_points=self.NAIROBI_ROAD_POINTS)

        @self.app.route('/check_road_traffic', methods=['POST'])
        def check_road_traffic():
            selected_roads = request.form.getlist('roads')
            road_traffic_data = {}

            for road_group in selected_roads:
                road_traffic_data[road_group] = self.get_road_traffic_data(
                    self.NAIROBI_ROAD_POINTS[road_group]
                )

            return jsonify(road_traffic_data)

    def run(self, debug=True, host='0.0.0.0', port=5000):
        self.app.run(debug=debug, host=host, port=port)




if __name__ == '__main__':
    tomtom_api_key = os.environ.get('TOMTOM_API_KEY', 'GPqt4YO1Fc5fmAXRCO4NKxESXljq4I7X')
    app = RoundaboutTrafficApp(tomtom_api_key)
    app.run()