from manim import *

class IntroScene(Scene):
    def construct(self):

        # Title
        title_text = Text("Habitable Zones around Main Sequence Stars", color=WHITE, font_size=36)
        subtitle_text = Text("AST320 - Louis Branch", color=WHITE, font_size=20)
        o_index = title_text.text.find("o", title_text.text.find("Zones"))
        title_text[o_index].set_color(YELLOW)
        title = VGroup(title_text, subtitle_text).arrange(DOWN, buff=0.1)
        self.add(title)

        # Citation
        citation_text = Text("Rushby et al (2013): ", color=WHITE, font_size=14)
        url_text = MarkupText("<u>10.1089/ast.2012.0938</u>", color=WHITE, font_size=14)
        citation = VGroup(citation_text, url_text).arrange(RIGHT, buff=0.1)
        citation.to_edge(DOWN + RIGHT, buff=0.5)
        self.add(citation)
        
        # Wait for 3 seconds
        self.wait(3)
        
        # Prepare the 'o' in "Zones" for independent animation
        # Creating a separate Text object for the 'o' so it can be animated independently
        o_text = Text("o", font_size=36, color=YELLOW).move_to(title_text[o_index].get_center())
        self.add(o_text)  # Ensure it's in the scene for the animation
        
        # Now, animate the 'o' moving to the center and fade out the rest of the text
        # Removing the original 'o' to avoid visual duplication
        title_text.remove(title_text[o_index])
        
        # Animate both the 'o' moving and the text fading
        self.play(
            o_text.animate.move_to(ORIGIN),
            FadeOut(title, citation),
            run_time=2  # Adjust the run_time as needed
        )

        star = Circle(radius=0.75, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        self.play(Transform(o_text, star))
        
        # Parameters for the orbits
        orbits = [
            #{"r": 0.1, "a": 3, "b": 2, "resonance": 1},
            {"r": 0.15, "a": 4.5, "b": 3, "resonance": 2},
            #{"r": 0.3, "a": 6, "b": 4, "resonance": 4},
        ]

        planet_paths = []  # To store ParametricFunction objects for each orbit
        planets = []
        for orbit in orbits:
            # Elliptical orbit
            orbit_path = ParametricFunction(
                lambda t: orbit["a"] * np.cos(t) * RIGHT + orbit["b"] * np.sin(t) * UP,
                t_range=np.array([0, TAU]),
                color=WHITE
            ).set_stroke(opacity=0.1)
            self.add(orbit_path)
            planet_paths.append(orbit_path)  # Add the path object to the list

            # Planet
            planet = Circle(radius=orbit["r"], color=BLUE, fill_opacity=1)
            planet.move_to(orbit_path.get_start())
            planets.append(planet)

            # Add planet to scene
            self.add(planet)

        animations = []
        for planet, orbit, orbit_path in zip(planets, orbits, planet_paths):
            # Correctly calculate a simplified orbit period based on the semi-major axis 'a'
            orbit_period = orbit["a"] ** 1.5  # Simplified, assuming units and constants are such that this calculation makes sense for visualization
            
            # Create an animation for the planet to move along its path
            animation = MoveAlongPath(planet, orbit_path, rate_func=linear, run_time=orbit_period)
            animations.append(animation)

        # Loop animations for a fixed duration or number of repeats
        number_of_repeats = 1
        for _ in range(number_of_repeats):  # Fixed number of repeats
            for animation in animations:
                self.play(animation, rate_func=linear)
