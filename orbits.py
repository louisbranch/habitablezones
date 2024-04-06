from typing import List, Dict
from manim import *

Start = Dict[str, object]
stars: List[Start] = [
    {"radius": 1, "scale": 1, "color": YELLOW, "inner": (0.8, 0.8), "outer": (1.2, 1.2)},
    {"radius": 0.5, "scale": 0.5, "color": PURE_RED, "inner": (0.6, 0.6), "outer": (0.8, 0.8)},
    {"radius": 1.5, "scale": 3, "color": PURE_BLUE, "inner": (1.2, 1.2), "outer": (1.4, 1.4)},
    {"radius": 1, "scale": 2/3, "color": YELLOW, "inner": (0.8, 0.8), "outer": (1.2, 1.2)},
]

def boundaries(scene, name, orbit, sizes, t=2):

    # Custom animation to interpolate between initial and final ellipses
    def update_ellipse(start, end):
        start_a, start_b = orbit * start
        end_a, end_b = orbit * end

        def update(obj, alpha):
            a = interpolate(start_a, end_a, alpha)
            b = interpolate(start_b, end_b, alpha)
            path = ParametricFunction(
                lambda t: a * np.cos(t) * RIGHT + b * np.sin(t) * UP,
                t_range=np.array([0, TAU]),
                color=WHITE
            )
            obj.become(DashedVMobject(path, num_dashes=50, dashed_ratio=0.5))

        return update

    a, b = orbit * sizes[0]
    path = ParametricFunction(
        lambda t: a * np.cos(t) * RIGHT + b * np.sin(t) * UP,
        t_range=np.array([0, TAU]),
        color=WHITE
    )

    ellipse = DashedVMobject(path, num_dashes=50, dashed_ratio=0.5)
    label = Text(name, font_size=16, color=WHITE).next_to(ellipse, DOWN, buff=0.1)
    scene.play(Create(ellipse), run_time=t)
    scene.add(label)

    def update_label(obj):
        obj.next_to(ellipse, DOWN)

    return (
        [
            UpdateFromAlphaFunc(ellipse, update_ellipse(sizes[0], sizes[1])),
            UpdateFromFunc(label, update_label),
        ],
        [
            UpdateFromAlphaFunc(ellipse, update_ellipse(sizes[1], sizes[2])),
            UpdateFromFunc(label, update_label),
        ],
        [
            UpdateFromAlphaFunc(ellipse, update_ellipse(sizes[2], sizes[3])),
            UpdateFromFunc(label, update_label),
        ],
    )
