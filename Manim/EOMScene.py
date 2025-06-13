from manim import *
import numpy as np


class GaussianBeamLenses(Scene):
    """
    A Manim scene that visualizes a Gaussian beam propagating between two lenses.
    The beam has its minimum waist exactly in the center of the optical system.
    This modified version shows the phase of the sine wave changing continuously
    after it enters a region marked by a rectangle.
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
        w0 = 0.4  # Beam waist at z=0
        zR = 3.0  # Rayleigh range

        # Function defining the beam radius w(z) along the propagation axis (z).
        def beam_waist(z):
            return w0 * np.sqrt(1 + (z / zR) ** 2)

        # --- OPTICAL ELEMENTS ---
        # The distance for the lenses and beam
        distance = 2 * np.pi
        z_range = [-distance, distance]

        # A dashed line representing the central optical axis
        center_line = DashedLine(
            start=LEFT * distance,
            end=RIGHT * distance,
            color=WHITE,
            stroke_opacity=0.7,
        )

        # Create lenses using the helper function
        lens1 = self.create_lens().move_to(LEFT * distance)
        lens2 = self.create_lens().move_to(RIGHT * distance)

        # --- BEAM PROFILE ---
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

        # --- RECTANGLE (MARKS THE START OF THE MEDIUM) ---
        rectangle = Rectangle(
            color=DARK_BLUE,
            width=12 * w0,
            height=6 * w0,
            fill_color=DARK_BLUE,
            fill_opacity=0.4,
        )
        rectangle.move_to(ORIGIN)

        # --- CONTINUOUS SINE WAVE (IN ONE PART) ---
        # Define the boundary where the phase modulation begins
        rect_left_x = -rectangle.width / 2

        # Define the phase modulation function using np.where for vectorization.
        # This function "turns on" the phase change at the boundary and continues it.
        def phase_modulation(t):
            # The phase modulation starts at the left edge of the rectangle.
            # To ensure continuity, we subtract the value of the modulation
            # at the starting point, so it smoothly grows from zero.
            start_phase_offset = np.sin(rect_left_x * 50e6)

            # Apply modulation only for t >= rect_left_x
            return np.where(t >= rect_left_x, np.sin(t * 5) - start_phase_offset, 0)

        # Create a single ParametricFunction for the entire sine wave.
        sine_function = ParametricFunction(
            lambda t: np.array(
                [t, beam_waist(t) * np.sin(t * 5 + phase_modulation(t)), 0]
            ),
            t_range=[z_range[0], z_range[1], 0.1],
            color="#8B0000",
            stroke_width=4,
        )

        # --- ANIMATION SEQUENCE ---
        # Fade in the optical elements
        self.play(
            FadeIn(lens1, scale=0.8),
            FadeIn(lens2, scale=0.8),
            FadeIn(rectangle, scale=0.8),
        )

        # Animate the creation of the beam envelope
        self.play(
            Create(center_line),
            FadeIn(beam_fill),
            Create(top_beam),
            Create(bottom_beam),
            run_time=2,
        )

        # Animate the creation of the single, continuous sine wave.
        self.play(Create(sine_function), run_time=3)

        # Hold the final scene for a moment
        self.wait(2)
