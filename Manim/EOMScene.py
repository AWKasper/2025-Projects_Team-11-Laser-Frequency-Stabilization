from manim import *
import numpy as np


class GaussianBeamLenses(Scene):
    """
    A Manim scene that visualizes a Gaussian beam propagating between two lenses.
    The beam has its minimum waist exactly in the center of the optical system.
    This modified version shows the phase of the sine wave changing continuously
    after it enters an Electro-Optic Modulator (EOM), represented by the rectangle.
    A formula for phase modulation is displayed above the EOM.
    """

    # This function creates a biconvex lens VGroup, making the code cleaner.
    def create_lens(self, lens_color=BLUE, fill_opacity=0.4):
        """Creates a closed, fillable biconvex lens Mobject."""
        # Define the top and bottom points of the lens
        p_top = [0, 1.8, 0]
        p_bottom = [0, -1.8, 0]

        # Create the two arcs that will form the lens outline.
        # We don't need to set the color here, as we'll do it on the final shape.
        right_arc = ArcBetweenPoints(p_top, p_bottom, angle=-PI / 2)
        left_arc = ArcBetweenPoints(p_top, p_bottom, angle=PI / 2)

        # Combine the two arcs into a single, continuous, closed path (VMobject).
        # This is the key to making the shape fillable. We trace the path
        # of the right_arc, then the left_arc in reverse order.
        lens_shape = VMobject()
        lens_shape.set_points_as_corners(
            [*right_arc.get_points(), *left_arc.reverse_points().get_points()]
        )

        # The .close_path() command ensures the start and end points are connected,
        # creating a sealed shape.
        lens_shape.close_path()

        # Now, apply the color and fill to the single, unified shape.
        # This will color the outline.
        lens_shape.set_stroke(color=lens_color)
        # This will fill the interior of the closed path.
        lens_shape.set_fill(color=lens_color, opacity=fill_opacity)

        return lens_shape

    def construct(self):
        # --- BEAM PARAMETERS AND FUNCTION ---
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

        # --- RECTANGLE (Represents an Electro-Optic Modulator) ---
        rectangle = Rectangle(
            color=DARK_BLUE,
            width=12 * w0,
            height=6 * w0,
            fill_color=DARK_BLUE,
            fill_opacity=0.4,
        )
        rectangle.move_to(ORIGIN)

        # --- EOM LABEL AND FORMULA ---
        # Create a text mobject for the label "E.O.M."
        eom_label = Tex("E.O.M.", color=WHITE).scale(0.7)
        # Position the label just below the top edge of the rectangle, centered.
        eom_label.next_to(rectangle.get_top(), DOWN, buff=0.3)

        # Create a MathTex mobject for the phase modulation formula.
        # This represents the carrier wave (frequency \omega_c) being modulated
        # by another sine wave (frequency \omega_m).
        formula = MathTex(
            r"y(t) \propto \sin(\omega_c t + \delta \sin(\omega_m t))", color=WHITE
        ).scale(0.8)
        # Position the formula above the EOM rectangle.
        formula.next_to(rectangle, UP, buff=0.5)

        # --- CONTINUOUS SINE WAVE (IN ONE PART) ---
        # Define the boundary where the phase modulation begins
        rect_left_x = -rectangle.width / 2

        # The original frequencies are extremely high (462e12 Hz for the carrier
        # and 22.848e6 Hz for modulation), which is physically realistic but not
        # visualizable in Manim. The animation would just be a solid red block.
        #
        # To make the effect visible, we significantly scale down both frequencies.
        # We choose new frequencies that create a clear visual distinction between
        # a "fast" carrier wave and a "slower" modulation.
        # The literal ratio of ~20,000 is too large to show both effects on screen,
        # so we use a more moderate ratio that demonstrates the principle of phase modulation.

        # Visual frequency for the main sine wave (carrier)
        f_carrier_vis = 25
        # Visual frequency for the phase modulation
        f_mod_vis = 2
        mod_amp = 0.1

        # Define the phase modulation function. It's active after the beam
        # enters the rectangle (Electro-Optic Modulator).
        def phase_modulation(t):
            start_phase_offset = np.sin(t * 40)
            # np.where is a vectorized conditional:
            # if t > rect_left_x, apply modulation, else return 0.
            return np.where(
                t > rect_left_x, mod_amp * np.sin(t * f_mod_vis) + start_phase_offset, 0
            )

        # Create a single ParametricFunction for the entire sine wave.
        # The sine wave's phase is modulated after it enters the rectangle.
        sine_function = ParametricFunction(
            lambda t: np.array(
                [t, beam_waist(t) * np.sin(t * f_carrier_vis + phase_modulation(t)), 0]
            ),
            t_range=[
                z_range[0],
                z_range[1],
                0.005,
            ],  # Use a smaller step for a smooth high-frequency wave
            color="#8B0000",
            stroke_width=2.5,  # A slightly thinner line can look cleaner
        )

        # --- ANIMATION SEQUENCE ---
        self.play(
            FadeIn(lens1, scale=0.8),
            FadeIn(lens2, scale=0.8),
            FadeIn(rectangle, scale=0.8),
            # Fade in the labels with the other elements
            FadeIn(eom_label),
            Write(formula),  # Animate the formula writing itself out
        )

        self.play(
            Create(center_line),
            # FadeIn(beam_fill), # The fill can be distracting from the sine wave
            Create(top_beam),
            Create(bottom_beam),
            run_time=2,
        )

        self.play(Create(sine_function), run_time=12)
        self.wait(3)
