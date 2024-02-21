import heapq
import random
import time, threading

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)

def heap_sort(arr):
    heapq.heapify(arr)
    sorted_arr = []
    while arr:
        sorted_arr.append(heapq.heappop(arr))
    return sorted_arr

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

def bucket_sort(arr):
    strings = [x for x in arr if isinstance(x, str)]
    numbers = [x for x in arr if isinstance(x, (int, float))]
    
    insertion_sort(strings)
    
    insertion_sort(numbers)
    
    # Combine the sorted lists
    sorted_arr = strings + numbers
    
    return sorted_arr

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

def timsort(arr):
    arr.sort()

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

def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while (swapped == True):
        swapped = False
        for i in range(start, end):
            if (arr[i] > arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if (swapped == False):
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if (arr[i] > arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1

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

def pancake_sort(arr):
    def flip(arr, i):
        arr[:i+1] = reversed(arr[:i+1])

    for curr_size in range(len(arr), 1, -1):
        max_idx = arr.index(max(arr[:curr_size]))
        if max_idx != curr_size - 1:
            if max_idx != 0:
                flip(arr, max_idx)
            flip(arr, curr_size - 1)

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

#bogosort
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

def bogosort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)

# Function to perform Strand Sort
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

def slow_sort(arr):
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    left = slow_sort(arr[:m])
    right = slow_sort(arr[m:])
    if left[-1] > right[-1]:
        left, right = right, left
    return left + right[:-1] + [left[-1]]

def stooge_sort(arr):
    if arr[0] > arr[-1]:
        arr[0], arr[-1] = arr[-1], arr[0]
    if len(arr) > 2:
        t = len(arr) // 3
        stooge_sort(arr[:len(arr)-t])
        stooge_sort(arr[t:])
        stooge_sort(arr[:len(arr)-t])

def bead_sort(arr):
    def transpose(beads):
        return [beads.count(i) for i in range(max(beads), 0, -1)]

    n = len(arr)
    beads = [0] * max(arr)
    for i in range(n):
        beads = [beads[j] + 1 if j < arr[i] else beads[j] for j in range(len(beads))]
    for _ in range(n):
        beads = transpose(beads)

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

def bozo_sort(arr):
    while not is_sorted(arr):
        a, b = random.sample(arr, 2)
        arr[arr.index(a)], arr[arr.index(b)] = arr[arr.index(b)], arr[arr.index(a)]

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

#Function for Tree Sort
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

#Function for Cube Sort
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

#Function for Pigeonhole Sort
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
