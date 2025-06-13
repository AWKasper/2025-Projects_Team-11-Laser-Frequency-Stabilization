from manim import *
from manim_physics import *


class AnimatedRayExampleScene(Scene):
    def construct(self):
        # Define the style for the lenses
        lens_style = {"fill_opacity": 0.25, "color": BLUE, "stroke_width": 2}

        # Create the two lenses
        lens1 = Lens(-5, 1, **lens_style).shift(LEFT * 4)
        lens2 = Lens(5, 1, **lens_style).shift(RIGHT * 4)

        # Instantly add the static lenses to the scene
        self.add(lens1, lens2)

        # --- Gaussian Beam Definition ---

        # Parameters for the Gaussian beam
        w0 = 0.1  # Beam waist (minimum radius)
        zR = 8  # Rayleigh range (controls divergence)

        # Function defining the beam waist w(z) along the propagation axis
        def beam_waist(z):
            return w0 * np.sqrt(1 + (z / zR) ** 2)

        # Create the top and bottom envelopes of the beam using ParametricFunction
        # The function takes a parameter 't' (which we use as the z-axis)
        # and returns a point [t, y(t), 0]
        top_beam = ParametricFunction(
            lambda z: [z, beam_waist(z), 0],
            t_range=[-7, 7, 0.1],  # t_range is [start, end, step]
            color=RED,
        )

        bottom_beam = ParametricFunction(
            lambda z: [z, -beam_waist(z), 0],
            t_range=[-7, 7, 0.1],
            color=RED,
        )

        # A center line for the beam
        center_line = DashedLine(
            start=LEFT * 7, end=RIGHT * 7, color=RED, stroke_opacity=0.5
        )

        # Animate the creation of the beam
        # We use Create to draw the Mobjects from left to right
        self.play(
            Create(top_beam, run_time=3),
            Create(bottom_beam, run_time=3),
            Create(center_line, run_time=3),
        )

        self.wait(1)  # Hold the final frame for a moment
