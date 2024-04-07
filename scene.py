from manim import *
import orbits, luminosity

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

        # Loop the orbit 2 times
        for _ in range(3):
            self.play(animation, rate_func=linear)

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

        # Loop the orbit once
        self.play(animation, rate_func=linear)

        inner_values = [np.array(orbit["inner"]) for orbit in orbits.stars]
        outer_values = [np.array(orbit["outer"]) for orbit in orbits.stars]

        ellipse = np.array([a, b])
        inner = orbits.boundaries(self, "Inner HZ", ellipse, inner_values)
        outer = orbits.boundaries(self, "Outer HZ", ellipse, outer_values)

        self.play(animation, rate_func=linear)

        for i, values in enumerate(orbits.stars):
            s = star.animate.scale(values["scale"]).set_color(values["color"])
            p  = planet.animate.set_color(values["planet"])
            self.play(s, p, *inner[i], *outer[i], run_time=5)

        self.play(animation, rate_func=linear)

class EquationScene(Scene):
    def highlight_equation(self, title, formula, highlights, times, highlight_color=YELLOW):
        timer = iter(times)
        
        def pause():
            return next(timer, 0)

        # Title
        title_text = Text(title, font_size=24)
        title_text.to_edge(UP)
        self.add(title_text)

        # Equation
        equation = MathTex(formula, substrings_to_isolate=highlights).scale(1.5)
        equation.next_to(title_text, DOWN, buff=0.5)
        self.add(equation)

        self.wait(pause())

        # Highlight loop
        for i, highlight in enumerate(highlights):
            self.play(Indicate(equation.get_part_by_tex(highlight), color=highlight_color), run_time=1)
            self.wait(pause())

        self.wait(pause())

        self.remove(title_text)
        self.remove(equation)

class StellarLuminosityScene(EquationScene):
    def construct(self):
        title = "Stellar Luminosity"
        formula = r"L = 4\pi R^2 \sigma T_{\text{eff}}^4"
        highlights = ["L", "R", "T"]
        self.highlight_equation(title, formula, highlights, [8, 9, 1, 1])

        title = "Proportionality"
        formula = r"L \propto R^2T^4"
        highlights = [r"\propto"]
        self.highlight_equation(title, formula, highlights, [2, 20])

        title = "Inverse Square Law"
        formula = r"1\over{r^2}"
        self.highlight_equation(title, formula, [], [14])

        title = "Stellar Luminosity"
        formula = r"L = 4\pi R^2 \sigma T_{\text{eff}}^4"
        self.highlight_equation(title, formula, [], [18, 12])
        
class HZBoundariesScene(EquationScene):
    def construct(self):
        title = "Habitable Zone Boundaries"
        formula = r"HZ = \left(L / {S(T_{\text{eff}})}\right)^{1/2}"
        highlights = ["HZ", "L", "S"]
        self.highlight_equation(title, formula, highlights, [7, 9, 1, 3])

        formula = r"HZ_{\text{inner}} = \left(L / {S_{\text{inner}}(T_{\text{eff}})}\right)^{1/2}"
        self.highlight_equation(title, formula, [], [12])

        formula = r"HZ_{\text{outer}} = \left(L / {S_{\text{outer}}(T_{\text{eff}})}\right)^{1/2}"
        self.highlight_equation(title, formula, [], [7])

        formula = r"HZ = \left(L / {S(T_{\text{eff}})}\right)^{1/2}"
        highlights = ["S", "L", "S"]
        self.highlight_equation(title, formula, highlights, [0, 8, 0, 39])

class HZTransitionRateScene(EquationScene):
    def construct(self):
        title = "Habitable Zone Transition Rate"
        formula = r"\mu = (HZ^\text{TMS} - HZ^\text{ZAMS} )/\tau"
        highlights = [r"\mu", r"HZ^\text{ZAMS}", r"HZ^\text{TMS}", r"\tau"]
        self.highlight_equation(title, formula, highlights, [17, 6, 2, 18, 50])

class ConclusionScene(Scene):
    def construct(self):

        # Title
        title_text = Text("Habitable Zone Lifetimes around Main Sequence Stars", color=WHITE, font_size=36)
        citation_text = Text("Rushby et al. (2013): ", color=WHITE, font_size=24)
        url_text = MarkupText("<u>10.1089/ast.2012.0938</u>", color=WHITE, font_size=24)
        title = VGroup(title_text, citation_text, url_text).arrange(DOWN, buff=0.1)
        self.add(title)
        
        self.wait(85)

        self.remove(title)
        
        title_text = Text("Are we alone in the Universe?", color=WHITE, font_size=36)
        o_index = title_text.text.find("o", title_text.text.find("alone"))
        title_text[o_index].set_color(YELLOW)
        self.add(title_text)

        # Prepare the 'o' in "Alone" for independent animation
        # Creating a separate Text object for the 'o' so it can be animated independently
        o_text = Text("o", font_size=36, color=YELLOW).move_to(title_text[o_index].get_center())
        self.add(o_text)  # Ensure it's in the scene for the animation
        
        # Now, animate the 'o' moving to the center and fade out the rest of the text
        # Removing the original 'o' to avoid visual duplication
        title_text.remove(title_text[o_index])
        
        # Animate both the 'o' moving and the text fading
        self.play(
            o_text.animate.move_to(ORIGIN),
            FadeOut(title_text),
            run_time=2 
        )

        star = Circle(radius=1, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        self.play(ReplacementTransform(o_text, star))
        self.wait(2)

        # Collapse the circle to a dot
        dot = Dot(point=star.get_center(), color=YELLOW)
        self.play(ReplacementTransform(star, dot))

        # Step 2: Transform the dot into text
        end_text = Text("The end.", font_size=36)
        self.play(ReplacementTransform(dot, end_text))
        self.wait(5)