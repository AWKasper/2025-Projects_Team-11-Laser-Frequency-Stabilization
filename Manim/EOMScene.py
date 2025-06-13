from manim import *
from manim_physics import *
import numpy as np

class GaussianRayExampleScene(Scene):
    def construct(self):
        # Define the style for the lenses
        lens_style = {"fill_opacity": 0.5, "color": BLUE}

        # Create the two lenses
        lens1 = Lens(-5, 1, **lens_style).shift(LEFT)
        lens2 = Lens(5, 1, **lens_style).shift(RIGHT)

        # --- MODIFIED SECTION ---
        # Parameters for the Gaussian beam simulation
        num_rays = 150  # Increased number of rays for a denser look
        beam_center = 0.0  # Center of the beam in the y-axis
        beam_width_std_dev = 0.75 # Standard deviation, controls the "width" of the beam

        # Generate starting y-positions from a Gaussian distribution
        ray_y_positions = np.random.normal(loc=beam_center, scale=beam_width_std_dev, size=num_rays)

        # Create a list of Ray objects with varying opacity to simulate a Gaussian intensity profile
        rays = []
        for y_pos in ray_y_positions:
            # Calculate opacity based on the Gaussian probability density function.
            # Rays closer to the center (y_pos ≈ beam_center) will have higher opacity.
            distance_from_center = abs(y_pos - beam_center)
            opacity = np.exp(-0.5 * (distance_from_center / beam_width_std_dev)**2)
            
            ray = Ray(
                start=LEFT * 5 + UP * y_pos,
                direction=RIGHT,
                init_length=5,
                propagate=[lens1, lens2],
                color=RED,
                stroke_width=1.5,
                stroke_opacity=opacity # Apply the calculated opacity
            )
            rays.append(ray)
        # --- END OF MODIFICATION ---

        # Instantly add the static lenses to the scene
        self.add(lens1, lens2)

        # Animate the creation of each ray simultaneously
        self.play(
            AnimationGroup(
                *[Create(ray) for ray in rays],
                lag_ratio=0.0,
                run_time=2 # Slightly longer animation for a smoother effect
            )
        )

        self.wait(2)
