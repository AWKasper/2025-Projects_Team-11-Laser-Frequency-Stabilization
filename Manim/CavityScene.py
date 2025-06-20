from manim import *
from manim_physics import *
import numpy as np

mirror_curvature = 4
mirror_height = 4
mirror_width = 1.5

class Spiegels(Scene):
    def construct(self):
        def beam(z):
            return 0.1 * np.sqrt(1 + (z / 1) ** 2)

        # Lens 1 maken door (later) verschil te nemen tussen een rechthoek en een cirkel
        spiegel1 = Rectangle(color=GRAY, fill_opacity=0.5, height=mirror_height, width=mirror_width)
        circle1 = Circle(radius=mirror_curvature)
        circle1.shift(2 * LEFT)
        spiegel1.shift(5.35 * LEFT)

        # Lens 2 maken door (later) verschil te nemen tussen rechthoek en cirkel
        spiegel2 = Rectangle(color=GRAY, fill_opacity=0.5, height=mirror_height, width=mirror_width)
        spiegel2.shift(5.35 * RIGHT)
        spiegel2.flip
        circle2 = Circle(radius=mirror_curvature)
        circle2.shift(2 * RIGHT)

        un = Difference(spiegel1, circle1, fill_opacity=0.5, color=GRAY)
        un2 = Difference(spiegel2, circle2, fill_opacity=0.5, color=GRAY)

        waist_top = ParametricFunction(lambda z: [z, beam(z), 0], t_range=(-10, 6), color=RED)
        waist_bottom = ParametricFunction(lambda z: [z, -beam(z), 0], t_range=(-10, 6), color=RED)
        wave = ParametricFunction(lambda z: [z, 0.1 * np.sqrt(1 + z ** 2) * np.sin(5 * z), 0], t_range=(-10, 6))

        # tijdsafhankelijke vorm van de sinus (ValueTracker houdt de tijd bij)
        t = ValueTracker(0)
        standing_wave = always_redraw(lambda: ParametricFunction(
            lambda z: [z, 0.1 * np.sqrt(1 + z ** 2) * np.sin(5 * z) * np.cos(8 * t.get_value()), 0], # Thanks naar Abe voor deze lambda functie
            t_range=(-6, 6),
            color=GREEN,
            use_vectorized=True
        ))

        exit_wave = always_redraw(lambda: ParametricFunction(lambda z: [z,0.1*np.sqrt(37)*np.abs(np.cos(4*t.get_value()))*np.sin(5*z),0],t_range=(6+0.1,8),color=WHITE,use_vectorized=True))



        self.play(Create(un), Create(un2), run_time=1)
        self.play(Create(waist_top), Create(waist_bottom))
        self.play(Create(wave))
        self.add(standing_wave)
        self.add(exit_wave)
        self.play(t.animate.increment_value(2 * np.pi), run_time=20, rate_func=linear)
