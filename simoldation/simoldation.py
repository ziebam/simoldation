import random
import struct

import moderngl_window as mglw
from math_utils import normalize_to_range, apply_mean_filter
from agent import Agent
from moderngl import POINTS, PROGRAM_POINT_SIZE


class Simoldation(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = viewpoint_width, viewpoint_height = (200, 200)

    framework_size = viewpoint_width * viewpoint_height

    population_percentage = 0.03
    population_size = round(population_percentage * framework_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.datamap = [
            [None for _ in range(self.viewpoint_width)]
            for _ in range(self.viewpoint_height)
        ]
        self.trailmap = [
            [0 for _ in range(self.viewpoint_width)]
            for _ in range(self.viewpoint_height)
        ]

        for _ in range(self.population_size):
            x = random.randint(0, self.viewpoint_width - 1)
            y = random.randint(0, self.viewpoint_height - 1)

            self.datamap[y][x] = Agent((y, x))

        self.trailmap_prog = self.ctx.program(
            vertex_shader="""
                #version 330 core
                in vec2 pos;
                in vec3 rgb;
                out vec3 greyscaleColor;

                void main() {
                    gl_Position = vec4(pos, 1.0, 1.0);
                    gl_PointSize = 3.0;
                    float gray = dot(rgb, vec3(0.21, 0.71, 0.07));
                    greyscaleColor = vec3(gray);
                }
            """,
            fragment_shader="""
                #version 330 core
                in vec3 greyscaleColor;
                out vec4 FragColor;

                void main() {
                    FragColor = vec4(greyscaleColor, 1.0);
                }
            """,
        )

    def render(self, time, frametime):
        self.ctx.enable_only(PROGRAM_POINT_SIZE)

        trails = [0, 0, 0, 0, 0]
        for y, row in enumerate(self.trailmap):
            for x, trail in enumerate(row):
                if trail > 0:
                    trail_x = normalize_to_range(x, (-1, 1), 0, self.viewpoint_width)
                    trail_y = normalize_to_range(y, (-1, 1), 0, self.viewpoint_height)
                    trail_rgb = normalize_to_range(trail, (0, 1), 0, 255)

                    trails.append(trail_x)
                    trails.append(trail_y)
                    trails.append(trail_rgb)
                    trails.append(trail_rgb)
                    trails.append(trail_rgb)

        self.trailmap_vbo = self.ctx.buffer(struct.pack(f"{len(trails)}f", *trails))
        self.trailmap_vao = self.ctx.vertex_array(
            self.trailmap_prog,
            [(self.trailmap_vbo, "2f 3f", "pos", "rgb")],
        )

        self.trailmap_vao.render(mode=POINTS)

        for row in self.datamap:
            for cell in row:
                if cell is not None:
                    cell.attempt_to_move_forward(self.datamap, self.trailmap)
                    cell.sensory_stage(self.trailmap)

        for y, row in enumerate(self.trailmap[1:-1]):
            for x, trail in enumerate(row[1:-1]):
                if trail > 0:
                    self.trailmap[y][x] -= 1
                self.trailmap[y][x] = apply_mean_filter((x, y), self.trailmap)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.ESCAPE:
                self.wnd.close()


if __name__ == "__main__":
    mglw.run_window_config(Simoldation)
