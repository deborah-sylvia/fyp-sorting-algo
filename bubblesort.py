from manim import *
from dataclasses import dataclass
from enum import Enum

# Define dataclasses for different events during sorting
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

# Define a union type for all event types
Event = BumpPointer | Compare | IndexSwap | Done

class Bubblesort(Scene):
    def construct(self):
        # Input list
        ls = [3, 2, 7, 6, 1, 5]

        # Create Manim objects for list elements and arrange them
        ls_manim = VGroup(*[Text(f'{n}') for n in ls])
        ls_manim.arrange()
        self.play(Create(ls_manim))  # Animate the creation of list elements

        events = []  # List to store events during sorting process
        self.sort(ls.copy(), events)  # Call the sorting algorithm

        ptr = Arrow(start=config.top + DOWN, end=config.top)  # Pointer for visualization during sorting

        last_compare = None  # Store the last comparison Text object
        for e in events:
            match e:
                case BumpPointer(idx):  # Event for updating pointer
                    self.play(ptr.animate.next_to(ls_manim[idx], direction=DOWN))
                case Compare(idx1, idx2):  # Event for comparing elements
                    sign = '<='
                    if ls[idx1] > ls[idx2]:
                        sign = '>'

                    if last_compare is not None:
                        self.remove(last_compare)

                    last_compare = Text(f'{ls[idx1]} {sign} {ls[idx2]}', font_size=36).next_to(ls_manim, direction=UP)
                    self.play(Create(last_compare))  # Animate the creation of comparison text
                case IndexSwap(idx1, idx2):  # Event for swapping elements
                    self.play(Swap(ls_manim[idx1], ls_manim[idx2]))  # Animate swapping of elements
                    ls_manim[idx1], ls_manim[idx2] = ls_manim[idx2], ls_manim[idx1]  # Update Manim objects
                    ls[idx1], ls[idx2] = ls[idx2], ls[idx1]  # Update list
                case Done(idx):  # Event indicating completion of sorting for an element
                    self.play(ls_manim[idx].animate.set_fill(GREEN))  # Animate setting the element to green

    # Sorting algorithm implementation
    def sort(self, ls: list[int], events: list[Event]):
        n = len(ls)
        for i in range(n):
            for j in range(1, n - i):
                events.append(BumpPointer(j))  # Add event for updating pointer
                events.append(Compare(j - 1, j))  # Add event for comparing elements
                if ls[j - 1] > ls[j]:  # Swap elements if they are in the wrong order
                    ls[j - 1], ls[j] = ls[j], ls[j - 1]
                    events.append(IndexSwap(j - 1, j))  # Add event for swapping elements
            events.append(Done(n - i - 1))  # Add event indicating completion of sorting for an element
