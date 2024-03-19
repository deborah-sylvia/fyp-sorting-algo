from manim import *
from dataclasses import dataclass

# Dataclasses to represent different events during Pigeonhole Sort
@dataclass
class CreatePigeonhole:
    mn: int  # Minimum value in the input list
    mx: int  # Maximum value in the input list

@dataclass
class AddToHole:
    val: int  # Value added to a pigeonhole

@dataclass
class MoveHoleToOutput:
    hole_idx: int  # Index of the pigeonhole
    to_idx: int  # Index where the pigeonhole elements are moved in the output list
    amount: int  # Number of elements moved from the pigeonhole to the output

@dataclass
class BumpPtr:
    idx: int  # Index pointer during sorting

Event = CreatePigeonhole | AddToHole | MoveHoleToOutput | BumpPtr  # Union type for all event types

# Scene for demonstrating Pigeonhole Sort
class Pigeonholesort(Scene):
    def construct(self):
        ls = [8, 4, 9, 3, 2, 4, 7, 3, 3]  # Input list

        ls_manim = VGroup(*[Text(f'{n}') for n in ls])  # Manim objects representing list elements
        ls_manim.arrange()  # Arrange elements in a horizontal row
        self.play(Create(ls_manim))  # Animate the creation of list elements

        events = []  # List to store events during sorting process
        self.sort(ls.copy(), events)  # Call the sorting algorithm

        pigeonholes = None  # Variable to store pigeonholes
        ptr = Arrow(start=config.top, end=config.top + DOWN)  # Arrow pointer for visualization

        offset = None  # Offset to adjust pigeonhole indices

        for e in events:
            match e:
                case CreatePigeonhole(mn, mx):
                    pigeonholes = [[] for _ in range(mn, mx + 1)]  # Initialize pigeonholes
                    offset = mn  # Set the offset for indexing

                    pigeonholes_text = Text('Pigeonholes', font_size=32).next_to(ls_manim, direction=DOWN)
                    self.play(Create(pigeonholes_text))  # Animate the creation of pigeonhole label

                    pigeonhole_labels = VGroup(*[Text(f'{n}', font_size=32, color=ORANGE, slant=ITALIC) for n in range(mn, mx + 1)])  # Labels for pigeonholes
                    pigeonhole_labels.arrange()  # Arrange labels
                    pigeonhole_labels.next_to(pigeonholes_text, direction=DOWN)  # Position labels
                    self.play(Create(pigeonhole_labels))  # Animate the creation of pigeonhole labels

                    self.play(Create(Line().next_to(pigeonhole_labels, direction=0.5 * DOWN)))  # Draw a line below labels

                case BumpPtr(idx):
                    self.play(ptr.animate.next_to(ls_manim[idx], direction=UP))  # Animate pointer movement
                case AddToHole(val):
                    pigeonhole = pigeonholes[val - offset]  # Get the corresponding pigeonhole
                    text = Text(f'{val}')  # Create text object for the value
                    if len(pigeonhole) == 0:
                        text.next_to(pigeonhole_labels[val - offset], direction=DOWN)  # Position text below label
                    else:
                        text.next_to(pigeonhole[-1], direction=DOWN)  # Position text below the last added element
                    pigeonhole.append(text)  # Add text to pigeonhole
                    self.play(Create(text))  # Animate the creation of text
                case MoveHoleToOutput(val, to_idx, amount):
                    self.remove(ptr)  # Remove pointer

                    pigeonhole = pigeonholes[val - offset]  # Get the corresponding pigeonhole
                    for i in range(amount):
                        prev_text = ls_manim[to_idx + i]  # Get the previous text object
                        x, y = prev_text.get_x(), prev_text.get_y()  # Get position of previous text
                        self.play(Transform(
                            ls_manim[to_idx + i],
                            Text(f'{val}').set_x(x).set_y(y).set_color(GREEN)  # Animate text transformation to the value in green color
                        ))
                        self.remove(pigeonhole[-1])  # Remove the last added element from the pigeonhole
                        pigeonhole.pop()  # Remove the last element from the pigeonhole

        self.wait()  # Wait at the end of the animation

    # Pigeonhole Sort algorithm implementation
    def sort(self, ls: list[int], events: list[Event]):
        mn, mx = min(ls), max(ls)  # Find minimum and maximum values in the list

        n = mx - mn + 1  # Calculate the number of pigeonholes
        pigeonholes = [[] for _ in range(n)]  # Initialize pigeonholes
        events.append(CreatePigeonhole(mn, mx))  # Add event for creating pigeonholes

        for i, v in enumerate(ls):
            events.append(BumpPtr(i))  # Add event for pointer movement
            pigeonholes[v - mn].append(v)  # Add value to corresponding pigeonhole
            events.append(AddToHole(v))  # Add event for adding value to pigeonhole

        cur = 0  # Initialize index for placing elements in the output list
        for i, pigeonhole in enumerate(pigeonholes):
            m = len(pigeonhole)  # Get the number of elements in the pigeonhole
            ls[cur:cur + m] = pigeonhole  # Place elements from pigeonhole to the output list
            events.append(MoveHoleToOutput(i + mn, cur, m))  # Add event for moving elements to output

            cur += m  # Update index for placing elements in the output list

# to run, run: manim -pql pigeonhole.py Pigeonholesort