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

@dataclass
class Done:
    index: int

Event = BumpPointer | Compare | IndexSwap | Done

class Bubblesort(Scene):
    def construct(self):
        ls = [3, 2, 7, 6, 1, 5]

        ls_manim = VGroup(*[Text(f'{n}') for n in ls])
        ls_manim.arrange()
        self.play(Create(ls_manim))

        events = []
        self.sort(ls.copy(), events)

        ptr = Arrow(start=config.top + DOWN, end=config.top)

        last_compare = None
        for e in events:
            match e:
                case BumpPointer(idx):
                    self.play(ptr.animate.next_to(ls_manim[idx], direction=DOWN))
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
                case Done(idx):
                    self.play(ls_manim[idx].animate.set_fill(GREEN))

    def sort(self, ls: list[int], events: list[Event]):
        n = len(ls)
        for i in range(n):
            for j in range(1, n - i):
                events.append(BumpPointer(j))
                events.append(Compare(j - 1, j))
                if ls[j - 1] > ls[j]:
                    ls[j - 1], ls[j] = ls[j], ls[j - 1]
                    events.append(IndexSwap(j - 1, j))
            events.append(Done(n - i - 1))

