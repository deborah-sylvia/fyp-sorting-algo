import time
import pandas as pd
from tqdm import tqdm
import algo
import os

def main():

    # Read the CSV file
    input_df = pd.read_csv("# location to dataset")
    arr = input_df[" # row that you want to sort"].tolist()
 
    sorting_algorithms = {
        "Selection Sort": algo.selection_sort,
        "Insertion Sort": algo.insertion_sort,
        "Bubble Sort": algo.bubble_sort,
        
        "Merge Sort": algo.merge_sort,
        "Quick Sort": algo.quick_sort,
        "Heap Sort": algo.heap_sort,
        
        "Radix Sort": algo.radix_sort,
        "Bucket Sort": algo.bucket_sort,
        "Counting Sort": algo.counting_sort,
        
        "Shell Sort": algo.shell_sort,
        "Tim Sort": algo.timsort,
        "Comb Sort": algo.comb_sort,
        "Cycle Sort": algo.cycle_sort,
        "Cocktail Sort": algo.cocktail_sort,
        "Gnome Sort": algo.gnome_sort,
        "Bitonic Sort": algo.bitonic_sort,
        # "Pancake Sort": algo.pancake_sort,
        "Binary Insertion Sort": algo.binary_insertion_sort,

        # "Bogo Sort": algo.bogosort,
        "Strand Sort": algo.strand_sort,
        # "Slow Sort": algo.slow_sort,
        # "Stooge Sort": algo.stooge_sort,
        # "Bead Sort": algo.bead_sort,
        # "Sleep Sort": algo.sleep_sort,
        # "Bozo Sort": algo.bozo_sort,
        # "Cocktail Shaker Sort": algo.cocktail_shaker_sort,
        "Odd-Even Sort": algo.odd_even_sort,
        "Tree Sort": algo.tree_sort,
        "Cube Sort": algo.cube_sort,
        "Pigeonhole Sort": algo.pigeonhole_sort,
    }

    if not isinstance(arr[0], int):
        sorting_algorithms.pop("Counting Sort")

    rows = []
    iterations = int(input("How many?\n"))
    for _ in tqdm(range(iterations)):
        row = {}
        for name, sort_f in sorting_algorithms.items():
            start = time.time()
            sort_f(arr.copy())
            end = time.time()
            row[name] = end - start
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.describe().to_csv(f"number_{iterations}.csv", index=True, header=True)

if __name__ == "__main__":
    main()
