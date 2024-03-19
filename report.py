import time  # Importing the time module for time-related operations
import pandas as pd  # Importing pandas library for data manipulation
from tqdm import tqdm  # Importing tqdm for progress bar visualization
import algo  # Importing the module containing sorting algorithms
import os  # Importing the os module for operating system dependent functionality

def main():
    # Read the CSV file
    input_df = pd.read_csv("/Users/syl/Desktop/FYP/IRL DATASETS/amazon_filtered.csv")  # Reading the CSV file
    arr = input_df["actual_price"].tolist()  # Converting the column to a list
    sorting_algorithms = {
        # Dictionary containing sorting algorithm names as keys and their corresponding functions as values
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

    if not isinstance(arr[0], int):  # Checking if the elements in the list are integers
        sorting_algorithms.pop("Counting Sort")  # If not, remove Counting Sort algorithm

    rows = []  # Initializing an empty list to store results
    iterations = int(input("How many?\n"))  # Getting the number of iterations from user
    for _ in tqdm(range(iterations)):  # Iterating over the specified number of iterations with a progress bar
        row = {}  # Initializing an empty dictionary for storing timing results of each algorithm
        for name, sort_f in sorting_algorithms.items():  # Iterating over sorting algorithms
            start = time.time()  # Recording the start time
            sort_f(arr.copy())  # Executing the sorting algorithm on a copy of the original list
            end = time.time()  # Recording the end time
            row[name] = end - start  # Calculating and storing the execution time
        rows.append(row)  # Appending the timing results for each algorithm to the rows list

    df = pd.DataFrame(rows)  # Creating a DataFrame from the timing results
    df.describe().to_csv(f"number_{iterations}.csv", index=True, header=True)  # Writing summary statistics to a CSV file

if __name__ == "__main__":
    main()  # Calling the main function if the script is executed directly
