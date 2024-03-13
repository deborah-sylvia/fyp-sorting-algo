from manim import *
from dataclasses import dataclass
from enum import Enum

@dataclass
class BumpPointer:
    index: int

@dataclass
class Compare:
    index1: int
    index2: int

@dataclass
class IndexSwap:
    index1: int
    index2: int

class IndexVariantChange(Enum):
    ODD = 1
    EVEN = 2

Event = BumpPointer | Compare | IndexSwap | IndexVariantChange

class Oddevensort(Scene):
    def construct(self):
        ls = [3, 2, 7, 6, 1, 5, 2, 10, 9]

        ls_manim = VGroup(*[Text(f'{n}') for n in ls])
        ls_manim.arrange()
        self.play(Create(ls_manim))

        events = []
        self.sort(ls.copy(), events)

        ptr1 = Arrow(start=config.top + DOWN, end=config.top)
        ptr2 = Arrow(start=config.top + DOWN, end=config.top)

        last_compare = None
        index_variant = None
        for e in events:
            match e:
                case BumpPointer(idx):
                    self.play(
                        ptr1.animate.next_to(ls_manim[idx], direction=DOWN),
                        ptr2.animate.next_to(ls_manim[idx + 1], direction=DOWN),
                    )
                case Compare(idx1, idx2):
                    sign = '<='
                    if ls[idx1] > ls[idx2]:
                        sign = '>'

                    if last_compare is not None:
                        self.remove(last_compare)

                    last_compare = Text(f'{ls[idx1]} {sign} {ls[idx2]}', font_size=36).next_to(ls_manim, direction=UP)
                    self.play(Create(last_compare))
                case IndexSwap(idx1, idx2):
                    self.play(Swap(ls_manim[idx1], ls_manim[idx2]))
                    ls_manim[idx1], ls_manim[idx2] = ls_manim[idx2], ls_manim[idx1]
                    ls[idx1], ls[idx2] = ls[idx2], ls[idx1]
                case IndexVariantChange.ODD | IndexVariantChange.EVEN:
                    if index_variant is not None:
                        self.remove(index_variant)
                    text = "Odd" if e == IndexVariantChange.ODD else "Even"
                    index_variant = Text(f'{text}').next_to(ls_manim, direction=3 * UP)
                    self.play(Create(index_variant))

    def sort(self, ls: list[int], events: list[Event]):
        n = len(ls)

        while True:
            done = True

            # Even
            events.append(IndexVariantChange.EVEN)
            for i in range(0, n - 1, 2):
                events.append(BumpPointer(i))
                events.append(Compare(i, i + 1))
                if ls[i] > ls[i + 1]:
                    done = False
                    ls[i], ls[i + 1] = ls[i + 1], ls[i]
                    events.append(IndexSwap(i, i + 1))

            # Odd
            events.append(IndexVariantChange.ODD)
            for i in range(1, n - 1, 2):
                events.append(BumpPointer(i))
                events.append(Compare(i, i + 1))
                if ls[i] > ls[i + 1]:
                    done = False
                    ls[i], ls[i + 1] = ls[i + 1], ls[i]
                    events.append(IndexSwap(i, i + 1))

            if done:
                break