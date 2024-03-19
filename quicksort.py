from manim import *
from dataclasses import dataclass
from enum import Enum

# Enum for different pointers used in the algorithm
class Pointer(Enum):
    LT_PIVOT_COUNT = 1  # Pointer to track the position for elements less than pivot
    I = 2  # Pointer for iterating through the list

# Dataclasses for different events in the sorting process
@dataclass
class InitPivot:
    index: int  # Event for initializing pivot

@dataclass
class Compare:
    index1: int  # Event for comparing elements during partitioning
    index2: int

@dataclass
class IndexSwap:
    index1: int  # Event for swapping elements during partitioning
    index2: int

@dataclass
class BumpPointer:
    ptr: Pointer  # Event for updating pointers during sorting
    new_index: int

@dataclass
class Done:
    start_index: int  # Event for indicating completion of sorting process
    end_index: int

Event = InitPivot | Compare | IndexSwap | BumpPointer | Done  # Union type for all event types

class Quicksort(Scene):
    def construct(self):
        ls = [8, 2, 3, 1, 5, 6, 4]  # Input list

        ls_manim = VGroup()  # Group to hold Manim objects representing list elements
        for n in ls:
            ls_manim.add(Text(f'{n}'))  # Create a Text object for each element
        ls_manim.arrange()  # Arrange elements in a horizontal row

        self.play(Create(ls_manim))  # Animate the creation of list elements

        events = []  # List to store events during sorting process
        self.sort(ls.copy(), events, 0, len(ls) - 1)  # Call the sorting algorithm

        # Pointers for visualization during sorting
        i_ptr_arrow = Arrow(start=config.top + DOWN, end=config.top)
        i_ptr_text = Text('i', font_size=24).next_to(i_ptr_arrow, direction=DOWN)
        i_ptr = Group(i_ptr_arrow, i_ptr_text)

        lt_pivot_count_ptr_arrow = Arrow(start=config.top + DOWN * 1.5, end=config.top)
        lt_pivot_count_ptr_text = Text('next pivot pos', font_size=24).next_to(lt_pivot_count_ptr_arrow, direction=DOWN)
        lt_pivot_count_ptr = Group(lt_pivot_count_ptr_arrow, lt_pivot_count_ptr_text)

        pivot_ptr_arrow = Arrow(start=config.top + DOWN, end=config.top)
        pivot_ptr_text = Text('pivot', font_size=24).next_to(pivot_ptr_arrow, direction=DOWN)
        pivot_ptr = Group(pivot_ptr_arrow, pivot_ptr_text)

        last_compare = None  # Store the last comparison Text object
        for e in events:
            match e:
                case Done(start_idx, end_idx):
                    self.play(*[ls_manim[i].animate.set_fill(GREEN) for i in range(start_idx, end_idx + 1)])
                case InitPivot(idx):
                    self.play(pivot_ptr.animate.next_to(ls_manim[idx], direction=DOWN))
                case Compare(idx1, idx2):
                    sign = '<'
                    if ls[idx1] >= ls[idx2]:
                        sign = '>='

                    if last_compare is not None:
                        self.remove(last_compare)

                    last_compare = Text(f'{ls[idx1]} {sign} {ls[idx2]} (pivot)', font_size=36).next_to(ls_manim, direction=UP)
                    self.play(Create(last_compare))

                case IndexSwap(idx1, idx2):
                    self.play(
                        Swap(ls_manim[idx1], ls_manim[idx2]),  # Animate swapping of elements
                        run_time=0.5,
                    )
                    ls_manim[idx1], ls_manim[idx2] = ls_manim[idx2], ls_manim[idx1]  # Update Manim objects
                    ls[idx1], ls[idx2] = ls[idx2], ls[idx1]  # Update list
                case BumpPointer(ptr, new_idx):
                    match ptr:
                        case Pointer.I:
                            self.play(i_ptr.animate.next_to(ls_manim[new_idx], direction=DOWN).shift(RIGHT * 0.1))
                        case Pointer.LT_PIVOT_COUNT:
                            self.play(lt_pivot_count_ptr.animate.next_to(ls_manim[new_idx], direction=DOWN).shift(LEFT * 0.1))

    # Quicksort algorithm implementation
    def sort(self, ls: list[int], events: list[Event], start: int, end: int):
        if start >= end:
            if start == end:
                events.append(Done(start, end))
            return
        m = self.partition(ls, events, start, end)
        self.sort(ls, events, start, m - 1)
        self.sort(ls, events, m + 1, end)
        events.append(Done(start, end))

    # Partitioning step of Quicksort
    def partition(self, ls: list[int], events: list[Event], start: int, end: int) -> int:
        events.append(InitPivot(end))  # Event for initializing pivot
        pivot = ls[end]

        lt_pivot_count = start
        events.append(BumpPointer(Pointer.LT_PIVOT_COUNT, start))  # Event for updating pointer

        for i in range(start, end):
            events.append(BumpPointer(Pointer.I, i))  # Event for updating pointer
            events.append(Compare(i, end))  # Event for comparing elements with pivot

            if ls[i] < pivot:
                events.append(IndexSwap(lt_pivot_count, i))  # Event for swapping elements
                ls[i], ls[lt_pivot_count] = ls[lt_pivot_count], ls[i]  # Swap elements

                events.append(BumpPointer(Pointer.LT_PIVOT_COUNT, lt_pivot_count + 1))  # Event for updating pointer
                lt_pivot_count += 1

        events.append(IndexSwap(lt_pivot_count, end))  # Event for swapping pivot into correct position
        ls[lt_pivot_count], ls[end] = ls[end], ls[lt_pivot_count]

        return lt_pivot_count
