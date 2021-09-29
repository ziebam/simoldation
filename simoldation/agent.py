import math
import random


class Agent:
    def __init__(
        self,
        position,
        sensor_angle=math.pi / 4,
        rotation_angle=math.pi / 4,
        sensor_offset=9,
        sensor_width=1,
        step_size=1,
        chemoattractant_deposition=5,
    ):
        self.position = self.pos_x, self.pos_y = position
        self.orientation = random.random() * 2 * math.pi
        self.sensor_angle = sensor_angle
        self.rotation_angle = rotation_angle
        self.sensor_offset = sensor_offset
        self.sensor_width = sensor_width
        self.step_size = step_size
        self.chemoattractant_deposition = chemoattractant_deposition

    def attempt_to_move_forward(self, datamap, trailmap):
        target_x = round(self.pos_x + math.cos(self.orientation))
        if target_x >= len(datamap[0]) or target_x < 0:
            target_x = self.pos_x

        target_y = round(self.pos_y + math.sin(self.orientation))
        if target_y >= len(datamap) or target_y < 0:
            target_y = self.pos_y

        if self.pos_x == target_x and self.pos_y == target_y:
            self.orientation = random.random() * 2 * math.pi
        if datamap[target_y][target_x] is None:
            datamap[self.pos_y][self.pos_x] = None
            self.position = self.pos_x, self.pos_y = target_x, target_y
            datamap[target_y][target_x] = self
            trailmap[target_y][target_x] += (
                self.chemoattractant_deposition
                if trailmap[target_y][target_x] <= 250
                else 0
            )
        else:
            self.orientation = random.random() * 2 * math.pi

    def sensory_stage(self, trailmap):
        f_x = round(self.pos_x + self.sensor_offset * math.cos(self.orientation))
        f_y = round(self.pos_y + self.sensor_offset * math.sin(self.orientation))

        fl_x = round(
            self.pos_x
            + self.sensor_offset * math.cos(self.orientation - self.rotation_angle)
        )
        fl_y = round(
            self.pos_y
            + self.sensor_offset * math.sin(self.orientation - self.rotation_angle)
        )

        fr_x = round(
            self.pos_x
            + self.sensor_offset * math.cos(self.orientation + self.rotation_angle)
        )
        fr_y = round(
            self.pos_y
            + self.sensor_offset * math.sin(self.orientation + self.rotation_angle)
        )

        if f_x >= len(trailmap[0]) or f_x < 0 or f_y >= len(trailmap) or f_y < 0:
            f = 0
        else:
            f = trailmap[f_y][f_x]

        if fl_x >= len(trailmap[0]) or fl_x < 0 or fl_y >= len(trailmap) or fl_y < 0:
            fl = 0
        else:
            fl = trailmap[fl_y][fl_x]

        if fr_x >= len(trailmap[0]) or fr_x < 0 or fr_y >= len(trailmap) or fr_y < 0:
            fr = 0
        else:
            fr = trailmap[fr_y][fr_x]

        if f < fl and f < fr:
            self.orientation += self.rotation_angle * (
                1 if random.random() < 0.5 else -1
            )
        elif fl < fr:
            self.orientation += self.rotation_angle
        elif fr < fl:
            self.orientation += -self.rotation_angle


# if __name__ == "__main__":
#     datamap = [[None for _ in range(10)] for _ in range(10)]
#     trailmap = [[0 for _ in range(10)] for _ in range(10)]

#     agent = Agent((5, 5))
#     datamap[5][5] = agent
#     print(datamap)
#     print(trailmap)
#     agent.attempt_to_move_forward(datamap, trailmap)
#     print(datamap)
#     print(trailmap)
