from manim import *
import numpy as np

mirror_curvature = 4
mirror_height = 4
mirror_width = 1.5

def beam(z):
    return 0.1 * np.sqrt(1 + (z / 1) ** 2)

class Spiegels(Scene):
      
    def construct(self):
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

        # Mirrors
        spiegel1 = Rectangle(color=GRAY, fill_opacity=0.5, height=mirror_height, width=mirror_width)
        circle1 = Circle(radius=mirror_curvature)
        circle1.move_to(spiegel1.get_center() + 2 * LEFT)
        spiegel1.shift(5.35 * LEFT)

        spiegel2 = Rectangle(color=GRAY, fill_opacity=0.5, height=mirror_height, width=mirror_width)
        circle2 = Circle(radius=mirror_curvature)
        circle2.move_to(spiegel2.get_center() + 2 * RIGHT)
        spiegel2.shift(5.35 * RIGHT)

        lens = create_lens(self)
        lens.move_to(6*LEFT)

        un = Difference(spiegel1, circle1, fill_opacity=0.5, color=GRAY)
        un2 = Difference(spiegel2, circle2, fill_opacity=0.5, color=GRAY)

        # Beam tracker
        beam_end = ValueTracker(-10)

        waist_top = always_redraw(lambda: ParametricFunction(
            lambda z: [z, beam(z), 0],
            t_range=(-6, beam_end.get_value()),
            color=RED
        ))

        waist_bottom = always_redraw(lambda: ParametricFunction(
            lambda z: [z, -beam(z), 0],
            t_range=(-6, beam_end.get_value()),
            color=RED
        ))

        # Group all visual components
        full_group = VGroup(un, un2, waist_top, waist_bottom)
        full_group.scale(0.6)  # 🔍 Scale down entire animation (adjust factor if needed)

        # Play mirror appearance
        self.play(FadeIn(un, scale=0.6), FadeIn(un2, scale=0.6), FadeIn(lens, scale=0.6))
        self.add(waist_top, waist_bottom)

        # Apply scale after elements are added
        self.add(full_group)

        # Animate beam growth
        self.play(beam_end.animate.set_value(3.5), run_time=3, rate_func=linear)

        self.wait(3)
