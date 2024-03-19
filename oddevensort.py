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

# Define an enumeration for index variant changes (odd/even)
class IndexVariantChange(Enum):
    ODD = 1
    EVEN = 2

# Define a union type for all event types
Event = BumpPointer | Compare | IndexSwap | IndexVariantChange

class Oddevensort(Scene):
    def construct(self):
        # Input list
        ls = [3, 2, 7, 6, 1, 5, 2, 10, 9]

        # Create Manim objects for list elements and arrange them
        ls_manim = VGroup(*[Text(f'{n}') for n in ls])
        ls_manim.arrange()
        self.play(Create(ls_manim))  # Animate the creation of list elements

        events = []  # List to store events during sorting process
        self.sort(ls.copy(), events)  # Call the sorting algorithm

        # Pointers for visualization during sorting
        ptr1 = Arrow(start=config.top + DOWN, end=config.top)
        ptr2 = Arrow(start=config.top + DOWN, end=config.top)

        last_compare = None  # Store the last comparison Text object
        index_variant = None  # Store the current index variant (odd/even)
        for e in events:
            match e:
                case BumpPointer(idx):  # Event for updating pointer
                    self.play(
                        ptr1.animate.next_to(ls_manim[idx], direction=DOWN),
                        ptr2.animate.next_to(ls_manim[idx + 1], direction=DOWN),
                    )
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
                case IndexVariantChange.ODD | IndexVariantChange.EVEN:  # Event indicating a change in index variant
                    if index_variant is not None:
                        self.remove(index_variant)
                    text = "Odd" if e == IndexVariantChange.ODD else "Even"
                    index_variant = Text(f'{text}').next_to(ls_manim, direction=3 * UP)
                    self.play(Create(index_variant))  # Animate the creation of index variant text

    # Sorting algorithm implementation
    def sort(self, ls: list[int], events: list[Event]):
        n = len(ls)

        while True:
            done = True

            # Even phase
            events.append(IndexVariantChange.EVEN)  # Add event indicating even phase
            for i in range(0, n - 1, 2):
                events.append(BumpPointer(i))  # Add event for updating pointer
                events.append(Compare(i, i + 1))  # Add event for comparing elements
                if ls[i] > ls[i + 1]:  # Swap elements if they are in the wrong order
                    done = False
                    ls[i], ls[i + 1] = ls[i + 1], ls[i]
                    events.append(IndexSwap(i, i + 1))  # Add event for swapping elements

            # Odd phase
            events.append(IndexVariantChange.ODD)  # Add event indicating odd phase
            for i in range(1, n - 1, 2):
                events.append(BumpPointer(i))  # Add event for updating pointer
                events.append(Compare(i, i + 1))  # Add event for comparing elements
                if ls[i] > ls[i + 1]:  # Swap elements if they are in the wrong order
                    done = False
                    ls[i], ls[i + 1] = ls[i + 1], ls[i]
                    events.append(IndexSwap(i, i + 1))  # Add event for swapping elements

            if done:  # Exit loop if no swaps were made in the current iteration
                break
