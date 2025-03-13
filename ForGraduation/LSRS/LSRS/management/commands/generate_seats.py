# generate_seats.py
from django.core.management import BaseCommand
from LSRS.models import Seats
from random import randint, choice, random


class Command(BaseCommand):
    help = '生成符合业务特征的座位数据'

    def handle(self, *args, **options):
        SEAT_CONFIG = {
            'A区': {
                'type_weights': {'normal': 0.4, 'corner': 0.2, 'VIP': 0.1, 'special': 0.3},
                'coords': {'x_range': (100, 300), 'y_range': (50, 450)},
                'power_prob': 0.7
            },
            'B区': {
                'type_weights': {'regular': 0.6, 'toilet': 0.05, 'corner': 0.35},
                'coords': {'x_range': (350, 650), 'y_range': (80, 400)},
                'power_prob': 0.4
            }
        }

        seat_counter = 1
        for zone, config in SEAT_CONFIG.items():
            for _ in range(100 if 'A区' in zone else 80):
                seat_type = self._weighted_choice(config['type_weights'])

                Seats.objects.create(
                    seat_id=int(f"{ord(zone[:1])}{seat_counter:03d}") , # 生成纯数字ID（示例：651001）[^3]
                seat_type=seat_type,
                    x_pos=randint(*config['coords']['x_range']),
                    y_pos=randint(*config['coords']['y_range']),
                    has_power=random() < config['power_prob'],
                    near_window=self._window_seat_logic(seat_type),
                    distance_to_door=self._calc_door_distance(zone),
                    status='available'
                )
                seat_counter += 1

    def _weighted_choice(self, weights):
        return max(weights.items(), key=lambda x: x[1] * random())[0]

    def _window_seat_logic(self, seat_type):
        return seat_type in ['corner', 'VIP'] and random() > 0.3

    def _calc_door_distance(self, zone):
        base_distance = {'A区': 8, 'B区': 12}.get(zone, 10)
        return randint(base_distance - 3, base_distance + 7)
