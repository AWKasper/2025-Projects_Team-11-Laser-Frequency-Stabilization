from manim import *
from manim_physics import *


class MaakLens(Scene):
    def construct(self):
        lens = Lens(2,1)  # create a circle
        lens.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(lens,height=0.01)) # show the circle on screen
        self.wait(10)