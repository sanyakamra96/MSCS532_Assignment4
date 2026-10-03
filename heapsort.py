"""Heapsort implementation for MSCS 532 Assignment 4."""


def heapify(arr, heap_size, root_index):
    """Restore the max-heap property for a subtree rooted at root_index."""
    largest = root_index
    left = 2 * root_index + 1
    right = 2 * root_index + 2

    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    if largest != root_index:
        arr[root_index], arr[largest] = arr[largest], arr[root_index]
        heapify(arr, heap_size, largest)


def build_max_heap(arr):
    """Transform arr into a max heap in O(n) time."""
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(arr, len(arr), i)


def heapsort(arr):
    """Sort arr in ascending order in place and return it."""
    build_max_heap(arr)
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        heapify(arr, end, 0)
    return arr


if __name__ == "__main__":
    sample = [12, 11, 13, 5, 6, 7]
    print("Original:", sample)
    print("Sorted:  ", heapsort(sample.copy()))
