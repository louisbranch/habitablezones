from manim import *
import orbits

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
        
        self.wait(10)
        
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
            run_time=2 
        )

        star = Circle(radius=1, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        self.play(Transform(o_text, star))

class PlanetarySystemScene(Scene):
    def construct(self):

        # Parameters for the orbits
        r = 1
        a, b = 4.5, 3

        star = Circle(radius=r, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        self.add(star)

        # Elliptical orbit
        orbit_path = ParametricFunction(
            lambda t: a * np.cos(t) * RIGHT + b * np.sin(t) * UP,
            t_range=np.array([0, TAU]),
            color=WHITE
        ).set_stroke(opacity=0.1)
        self.add(orbit_path)

        # Planet
        planet = Circle(0.15, color=BLUE, fill_opacity=1)
        planet.move_to(orbit_path.get_start())
        self.add(planet)

        # Correctly calculate a simplified orbit period based on the semi-major axis 'a'
        orbit_period = a ** 1.5
        animation = MoveAlongPath(planet, orbit_path, rate_func=linear, run_time=orbit_period)
        self.play(animation, rate_func=linear)

        inner_values = [np.array(orbit["inner"]) for orbit in orbits.stars]
        outer_values = [np.array(orbit["outer"]) for orbit in orbits.stars]

        ellipse = np.array([a, b])
        inner = orbits.boundaries(self, "Inner HZ", ellipse, inner_values)
        outer = orbits.boundaries(self, "Outer HZ", ellipse, outer_values)

        for i, values in enumerate(orbits.stars):
            if i == 0:
                continue # skip original star
            
            scale = star.animate.scale(values["scale"])
            color = star.animate.set_color(values["color"])
            #atm  = planet.animate.set_color
            
            self.play(scale, color, *inner[i-1], *outer[i-1], run_time=2)


class EquationScene(Scene):
    def highlight_equation(self, title, formula, highlights, highlight_color=YELLOW, wait_time=2):
        # Title
        title_text = Text(title, font_size=24)
        title_text.to_edge(UP)
        self.add(title_text)

        # Equation
        equation = MathTex(formula, substrings_to_isolate=highlights).scale(1.5)
        equation.next_to(title_text, DOWN, buff=0.5)
        self.add(equation)

        # Highlight loop
        for highlight in highlights:
            self.play(Indicate(equation.get_part_by_tex(highlight), color=highlight_color), run_time=1)
            self.wait(wait_time)

class StellarLuminosityScene(EquationScene):
    def construct(self):
        title = "Stellar Luminosity"
        formula = r"L = 4\pi R^2 \sigma T_{\text{eff}}^4"
        highlights = ["L", "R", "\sigma", "T"]
        self.highlight_equation(title, formula, highlights)

class HZBoundariesScene(EquationScene):
    def construct(self):
        title = "Habitable Zone Boundaries"
        formula = r"\text{HZ}_{\text{inner/outer}} = \frac{L}{S_{\text{inner/outer}}(T_{\text{eff}})}"
        highlights = ["HZ", "L", "S", "T"]
        self.highlight_equation(title, formula, highlights)

class HZTransitionRateScene(EquationScene):
    def construct(self):
        title = "Habitable Zone Transition Rate"
        formula = r"\mu_{\text{inner/outer}} = \frac{\text{HZ}_{\text{inner/outer}}^{\text{TMS}} - \text{HZ}_{\text{inner/outer}}^{\text{ZAMS}}}{\tau}"
        highlights = ["\mu", "HZ", "HZ", "\tau"]
        self.highlight_equation(title, formula, highlights, highlight_color=RED, wait_time=1.5)
