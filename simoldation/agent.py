import math
import random

from math_utils import apply_pbcs


class Agent:
    def __init__(
        self,
        pos_x,
        pos_y,
        sensor_angle=math.pi / 4,
        rotation_angle=math.pi / 4,
        sensor_offset=9,
        step_size=1,
        chemoattractant_deposition=5,
    ):
        # TODO Docstring.
        self.pos_x, self.pos_y = pos_x, pos_y
        self.sensor_angle = sensor_angle
        self.rotation_angle = rotation_angle
        self.sensor_offset = sensor_offset
        self.step_size = step_size
        self.chemoattractant_deposition = chemoattractant_deposition

        self.orientation = 2 * math.pi * random.random()

    def motor_stage(self, datamap, trailmap):
        # TODO Docstring.
        width = len(datamap[0])
        height = len(datamap)

        target_x = round(self.pos_x + self.step_size * math.cos(self.orientation))
        target_y = round(self.pos_y + self.step_size * math.sin(self.orientation))

        target_x = apply_pbcs(target_x, width)
        target_y = apply_pbcs(target_y, height)

        if datamap[target_y][target_x] is None:
            datamap[self.pos_y][self.pos_x] = None
            datamap[target_y][target_x] = self
            self.pos_x, self.pos_y = target_x, target_y

            if trailmap[target_y][target_x] <= 250:
                trailmap[target_y][target_x] += self.chemoattractant_deposition
        else:
            self.orientation = 2 * math.pi * random.random()

    def sensory_stage(self, trailmap):
        # TODO Docstring.
        width = len(trailmap[0])
        height = len(trailmap)

        front_x = round(self.pos_x + self.sensor_offset * math.cos(self.orientation))
        front_y = round(self.pos_y + self.sensor_offset * math.sin(self.orientation))

        angle_counterclockwise = self.orientation - self.rotation_angle
        left_x = round(
            self.pos_x + self.sensor_offset * math.cos(angle_counterclockwise)
        )
        left_y = round(
            self.pos_y + self.sensor_offset * math.sin(angle_counterclockwise)
        )

        angle_clockwise = self.orientation + self.rotation_angle
        right_x = round(self.pos_x + self.sensor_offset * math.cos(angle_clockwise))
        right_y = round(self.pos_y + self.sensor_offset * math.sin(angle_clockwise))

        front_x = apply_pbcs(front_x, width)
        front_y = apply_pbcs(front_y, height)
        left_x = apply_pbcs(left_x, width)
        left_y = apply_pbcs(left_y, height)
        right_x = apply_pbcs(right_x, width)
        right_y = apply_pbcs(right_y, height)

        front_sample = trailmap[front_y][front_x]
        left_sample = trailmap[left_y][left_x]
        right_sample = trailmap[right_y][right_x]

        if front_sample < left_sample and front_sample < right_sample:
            self.orientation += self.rotation_angle * (
                1 if random.random() < 0.5 else -1
            )
        elif left_sample < right_sample:
            self.orientation += self.rotation_angle
        elif right_sample < left_sample:
            self.orientation += -self.rotation_angle
