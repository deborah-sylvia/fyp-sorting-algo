from manim import *
from dataclasses import dataclass

@dataclass
class CreatePigeonhole:
    mn: int
    mx: int

@dataclass
class AddToHole:
    val: int

@dataclass
class MoveHoleToOutput:
    hole_idx: int
    to_idx: int
    amount: int

@dataclass
class BumpPtr:
    idx: int

Event = CreatePigeonhole | AddToHole | MoveHoleToOutput | BumpPtr


class Pigeonholesort(Scene):
    def construct(self):
        ls = [8, 4, 9, 3, 2, 4, 7, 3, 3]

        ls_manim = VGroup(*[Text(f'{n}') for n in ls])
        ls_manim.arrange()
        self.play(Create(ls_manim))

        events = []
        self.sort(ls.copy(), events)

        pigeonholes = None
        ptr = Arrow(start=config.top, end=config.top + DOWN)

        offset = None

        for e in events:
            match e:
                case CreatePigeonhole(mn, mx):
                    pigeonholes = [[] for _ in range(mn, mx + 1)]
                    offset = mn

                    pigeonholes_text = Text('Pigeonholes', font_size=32).next_to(ls_manim, direction=DOWN)
                    self.play(Create(pigeonholes_text))

                    pigeonhole_labels = VGroup(*[Text(f'{n}', font_size=32, color=ORANGE, slant=ITALIC) for n in range(mn, mx + 1)])
                    pigeonhole_labels.arrange()
                    pigeonhole_labels.next_to(pigeonholes_text, direction=DOWN)
                    self.play(Create(pigeonhole_labels))

                    self.play(Create(Line().next_to(pigeonhole_labels, direction=0.5 * DOWN)))

                case BumpPtr(idx):
                    self.play(ptr.animate.next_to(ls_manim[idx], direction=UP))
                case AddToHole(val):
                    pigeonhole = pigeonholes[val - offset]
                    text = Text(f'{val}')
                    if len(pigeonhole) == 0:
                        text.next_to(pigeonhole_labels[val - offset], direction=DOWN)
                    else:
                        text.next_to(pigeonhole[-1], direction=DOWN)

                    pigeonhole.append(text)
                    self.play(Create(text))
                case MoveHoleToOutput(val, to_idx, amount):
                    self.remove(ptr)

                    pigeonhole = pigeonholes[val - offset]
                    for i in range(amount):
                        prev_text = ls_manim[to_idx + i]
                        x, y = prev_text.get_x(), prev_text.get_y()
                        self.play(Transform(
                            ls_manim[to_idx + i],
                            Text(f'{val}').set_x(x).set_y(y).set_color(GREEN)
                        ))
                        self.remove(pigeonhole[-1])
                        pigeonhole.pop()


        self.wait()

    def sort(self, ls: list[int], events: list[Event]):
        mn, mx = min(ls), max(ls)

        n = mx - mn + 1
        pigeonholes = [[] for _ in range(n)]
        events.append(CreatePigeonhole(mn, mx))

        for i, v in enumerate(ls):
            events.append(BumpPtr(i))
            pigeonholes[v - mn].append(v)
            events.append(AddToHole(v))

        cur = 0
        for i, pigeonhole in enumerate(pigeonholes):
            m = len(pigeonhole)
            ls[cur:cur + m] = pigeonhole
            events.append(MoveHoleToOutput(i + mn, cur, m))

            cur += m

# to run, run: manim -pql pigeonhole.py Pigeonholesort