from manim import *
import numpy as np


class GaussianBeamLenses(Scene):
    """
    A Manim scene that visualizes a Gaussian beam propagating between two lenses.
    The beam has its minimum waist exactly in the center of the optical system.
    This version uses taller lenses and a wider beam to better fill the vertical space.
    """

    # This function creates a biconvex lens VGroup, making the code cleaner.
    def create_lens(self, lens_color=BLUE, fill_opacity=0.4):
        """Creates a taller biconvex lens Mobject."""
        # Increased y-values to make the lens taller
        p_top = [0, 1.8, 0]
        p_bottom = [0, -1.8, 0]
        # Right arc of the lens
        arc1 = ArcBetweenPoints(p_top, p_bottom, angle=-PI / 2, color=lens_color)
        # Left arc of the lens
        arc2 = ArcBetweenPoints(p_top, p_bottom, angle=PI / 2, color=lens_color)
        lens_shape = VGroup(arc1, arc2).set_fill(lens_color, opacity=fill_opacity)
        return lens_shape

    def construct(self):
        # --- BEAM PARAMETERS AND FUNCTION ---
        # These parameters define the shape and divergence of the beam.
        # Increased beam waist (w0) to make the beam thicker
        w0 = 0.4
        zR = 3.0  # Rayleigh range (adjusted for the shorter distance)

        # Function defining the beam radius w(z) along the propagation axis (z).
        def beam_waist(z):
            return w0 * np.sqrt(1 + (z / zR) ** 2)

        # --- OPTICAL ELEMENTS ---
        # The distance for the lenses and beam
        distance = 4.0

        # A dashed line representing the central optical axis
        center_line = DashedLine(
            start=LEFT * (distance + 0.5),
            end=RIGHT * (distance + 0.5),
            color=WHITE,
            stroke_opacity=0.7,
        )

        # Create lenses using the helper function
        lens1 = self.create_lens().move_to(LEFT * distance)
        lens2 = self.create_lens().move_to(RIGHT * distance)

        # --- BEAM PROFILE ---
        # The z-range over which the beam is drawn, matching the lens distance
        z_range = [-distance, distance]

        # The top envelope of the beam
        top_beam = ParametricFunction(
            lambda z: [z, beam_waist(z), 0],
            t_range=[z_range[0], z_range[1], 0.1],
            color=RED,
        )
        # The bottom envelope of the beam
        bottom_beam = ParametricFunction(
            lambda z: [z, -beam_waist(z), 0],
            t_range=[z_range[0], z_range[1], 0.1],
            color=RED,
        )

        # Create a Polygon to fill the space between the top and bottom envelopes
        beam_points_top = top_beam.get_points()
        beam_points_bottom = bottom_beam.get_points()
        beam_fill = Polygon(
            *np.concatenate([beam_points_top, beam_points_bottom[::-1]]),
            stroke_width=0,
            fill_color=RED,
            fill_opacity=0.4
        )

        # --- ANIMATION SEQUENCE ---
        self.play(FadeIn(lens1, scale=0.8), FadeIn(lens2, scale=0.8))

        # Animate the creation of the beam
        self.play(
            Create(center_line), Create(top_beam), Create(bottom_beam), run_time=2
        )
        self.play(FadeIn(beam_fill), run_time=1.5)

        # Hold the final scene
        self.wait(1)
