import heapq
import random
import time, threading

# Selection Sort: Sorts an array by repeatedly finding the minimum element from the unsorted part and moving it to the beginning.
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        # Find the index of the minimum element in the unsorted part
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_index] = arr[min_index], arr[i]

# Insertion Sort: Builds the final sorted array one item at a time by repeatedly moving elements to their correct position.
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1] that are greater than key to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Merge Sort: Divide the unsorted array into two halves, sort each half, and then merge them.
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Merge the two sorted halves into a single sorted array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Check for any remaining elements in left_half and right_half and add them to the sorted array
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Quick Sort: Picks a pivot element and partitions the array around the pivot, such that elements smaller than the pivot are on its left and larger elements are on its right.
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)

# Heap Sort: Builds a heap from the input array and then repeatedly extracts the maximum element from the heap and rebuilds the heap until the array is sorted.
def heap_sort(arr):
    heapq.heapify(arr)
    sorted_arr = []
    while arr:
        sorted_arr.append(heapq.heappop(arr))
    return sorted_arr

# Counting Sort: Works by counting the number of occurrences of each unique element in the input array and using arithmetic to determine the positions of each element in the sorted output array.
def counting_sort(arr: list[int]) -> list[int]:
    max_val = max(arr)
    min_val = min(arr)
    count = [0] * (max_val - min_val + 1)
    for num in arr:
        count[num - min_val] += 1
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i + min_val] * count[i])
    return sorted_arr

# Radix Sort: Sorts numbers by considering individual digits at different positions, starting from the least significant digit to the most significant digit.
def radix_sort(arr):
    # Sorting function for mixed data types
    numeric_values = []
    string_values = []
    for value in arr:
        if isinstance(value, (int, float)) or value.isnumeric():
            numeric_values.append(value)
        else:
            string_values.append(value)

    # Sort numeric values
    numeric_values = sorted(numeric_values, key=lambda x: float(x))

    # Sort string values
    string_values = sorted(string_values)

    # Combine the sorted lists
    sorted_arr = numeric_values + string_values
    return sorted_arr

# Bucket Sort: Distributes the elements of an array into a number of buckets, then sorts each bucket individually, and finally merges the buckets.
def bucket_sort(arr):
    strings = [x for x in arr if isinstance(x, str)]
    numbers = [x for x in arr if isinstance(x, (int, float))]

    insertion_sort(strings)
    insertion_sort(numbers)

    # Combine the sorted lists
    sorted_arr = strings + numbers
    return sorted_arr

# Bubble Sort: Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break

# Shell Sort: An extension of insertion sort that allows the exchange of items that are far apart, thus producing partially sorted arrays that can be efficiently sorted.
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

# Timsort: A hybrid sorting algorithm derived from merge sort and insertion sort, designed to perform well on many kinds of real-world data.
def timsort(arr):
    arr.sort()

# Comb Sort: Improves on bubble sort by using a gap of size more than 1 and by shrinking the gap with each iteration.
def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3
    swapped = True
    while gap > 1 or swapped:
        gap = max(1, int(gap / shrink))
        swapped = False
        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True

# Cycle Sort: A sorting algorithm that is theoretically optimal for uniformly distributed data, minimizing the number of memory writes to sort.
def cycle_sort(arr):
    n = len(arr)
    for cycle_start in range(n - 1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]

# Cocktail Sort: A variation of bubble sort that sorts in both directions, rather than one, each pass through the array.
def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped == True:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if swapped == False:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1

# Gnome Sort: A sorting algorithm similar to insertion sort but moving elements to the correct position by a series of swaps, similar to how a gnome sorts out flower pots.
def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0:
            index = 1
        if arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1

# Bitonic Sort: A parallel sorting algorithm based on the concept of merging two bitonic sequences (sequences that are initially monotonically increasing and then monotonically decreasing).
def bitonic_sort(arr):
    def bitonic_merge(arr, up):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        if up:
            bitonic_compare(arr, mid, True)
        bitonic_merge(arr[:mid], up)
        bitonic_merge(arr[mid:], up)

    def bitonic_compare(arr, n, up):
        k = n // 2
        for i in range(k):
            if (arr[i] > arr[i + k]) == up:
                arr[i], arr[i + k] = arr[i + k], arr[i]

    def bitonic_sort_recursive(arr, up):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        bitonic_sort_recursive(arr[:mid], True)
        bitonic_sort_recursive(arr[mid:], False)
        bitonic_merge(arr, up)

    bitonic_sort_recursive(arr, True)

# Pancake Sort: A sorting algorithm that sorts a sequence by flipping the elements of the array like pancakes.
def pancake_sort(arr):
    def flip(arr, i):
        arr[:i+1] = reversed(arr[:i+1])

    for curr_size in range(len(arr), 1, -1):
        max_idx = arr.index(max(arr[:curr_size]))
        if max_idx != curr_size - 1:
            if max_idx != 0:
                flip(arr, max_idx)
            flip(arr, curr_size - 1)

# Binary Insertion Sort: An enhancement of insertion sort that uses binary search to find the correct location to insert the current element.
def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        x = arr[i]
        left, right = 0, i - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < x:
                left = mid + 1
            else:
                right = mid - 1
        arr[left + 1:i + 1] = arr[left:i]
        arr[left] = x

# Bogosort: A highly ineffective sorting algorithm that generates random permutations of the input array until it finds one that is sorted.
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

def bogosort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)

# Strand Sort: A sorting algorithm that repeatedly pulls sorted sublists out of the input array and merges them with a result array.
def strand_sort(arr):
    result = []
    while arr:
        sublist = [arr.pop(0)]
        i = 0
        while i < len(arr):
            if arr[i] > sublist[-1]:
                sublist.append(arr.pop(i))
            else:
                i += 1
        result = merge(result, sublist)
    return result

def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result += left
    result += right
    return result

# Slow Sort: An intentionally inefficient sorting algorithm used for educational purposes, based on a divide-and-conquer approach.
def slow_sort(arr):
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    left = slow_sort(arr[:m])
    right = slow_sort(arr[m:])
    if left[-1] > right[-1]:
        left, right = right, left
    return left + right[:-1] + [left[-1]]

# Stooge Sort: A recursive sorting algorithm that sorts the first 2/3 and the last 2/3 of an array recursively and then sorts the first 2/3 again.
def stooge_sort(arr):
    if arr[0] > arr[-1]:
        arr[0], arr[-1] = arr[-1], arr[0]
    if len(arr) > 2:
        t = len(arr) // 3
        stooge_sort(arr[:len(arr)-t])
        stooge_sort(arr[t:])
        stooge_sort(arr[:len(arr)-t])

# Bead Sort: A natural sorting algorithm inspired by beads on an abacus, where elements are sorted by moving the beads to their appropriate positions.
def bead_sort(arr):
    def transpose(beads):
        return [beads.count(i) for i in range(max(beads), 0, -1)]

    n = len(arr)
    beads = [0] * max(arr)
    for i in range(n):
        beads = [beads[j] + 1 if j < arr[i] else beads[j] for j in range(len(beads))]
    for _ in range(n):
        beads = transpose(beads)

# Sleep Sort: A sorting algorithm that sorts integers by creating a separate thread for each element and sleeping for a duration proportional to its value.
def sleep_sort(arr):
    sorted_arr = []

    def worker(x):
        time.sleep(x)
        sorted_arr.append(x)

    threads = []
    for num in arr:
        thread = threading.Thread(target=worker, args=(num,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    arr[:] = sorted_arr

# Bozo Sort: An inefficient and humorous sorting algorithm that randomly shuffles the input array until it becomes sorted.
def bozo_sort(arr):
    while not is_sorted(arr):
        a, b = random.sample(arr, 2)
        arr[arr.index(a)], arr[arr.index(b)] = arr[arr.index(b)], arr[arr.index(a)]

# Odd-Even Sort: A variation of bubble sort that works in parallel by comparing and swapping pairs of elements in alternating odd-even passes.
def odd_even_sort(arr):
    n = len(arr)
    sorted = False
    while not sorted:
        sorted = True
        for i in range(1, n-1, 2):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                sorted = False
        for i in range(0, n-1, 2):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                sorted = False

# Tree Sort: A sorting algorithm that builds a binary search tree from the elements of the input array and performs an in-order traversal to obtain the sorted sequence.
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def in_order_traversal(root, result):
    if root:
        in_order_traversal(root.left, result)
        result.append(root.val)
        in_order_traversal(root.right, result)

def tree_sort(arr):
    root = None
    for item in arr:
        root = insert(root, item)
    result = []
    in_order_traversal(root, result)
    return result

# Cube Sort: A sorting algorithm that sorts a list of numbers by recursively partitioning them into sublists and then sorting each sublist using the cube sort algorithm.
def cube_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            for j in range(i - gap, -1, -gap):
                if arr[j] > arr[j + gap]:
                    arr[j], arr[j + gap] = arr[j + gap], arr[j]
        gap //= 2
    return arr

# Pigeonhole Sort: A sorting algorithm that is suitable for sorting lists of elements where the number of elements and the range of possible key values are approximately the same.
def pigeonhole_sort(arr):
    # Determine the minimum and maximum values in arr
    if all(isinstance(x, (int, float)) for x in arr):
        min_val, max_val = min(arr), max(arr)
        pigeonholes = [0] * (int(max_val) - int(min_val) + 1)
        for num in arr:
            pigeonholes[int(num) - int(min_val)] += 1
        sorted_arr = []
        for i in range(len(pigeonholes)):
            sorted_arr.extend([i + int(min_val)] * pigeonholes[i])
    else:
        # If elements are not numeric, sort them as strings
        sorted_arr = sorted(arr)
    
    return sorted_arr
