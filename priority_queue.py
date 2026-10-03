"""Max-heap priority queue for MSCS 532 Assignment 4."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Task:
    task_id: str
    priority: int
    arrival_time: int = 0
    deadline: Optional[int] = None

    def __repr__(self):
        return (
            f"Task(id={self.task_id!r}, priority={self.priority}, "
            f"arrival={self.arrival_time}, deadline={self.deadline})"
        )


class MaxPriorityQueue:
    """Array-backed max heap with an index map for efficient key updates."""

    def __init__(self):
        self.heap: List[Task] = []
        self.position: Dict[str, int] = {}

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i].task_id] = i
        self.position[self.heap[j].task_id] = j

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent].priority >= self.heap[index].priority:
                break
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index: int) -> None:
        n = len(self.heap)
        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2
            if left < n and self.heap[left].priority > self.heap[largest].priority:
                largest = left
            if right < n and self.heap[right].priority > self.heap[largest].priority:
                largest = right
            if largest == index:
                break
            self._swap(index, largest)
            index = largest

    def insert(self, task: Task) -> None:
        if task.task_id in self.position:
            raise ValueError(f"Task ID {task.task_id!r} already exists")
        self.heap.append(task)
        index = len(self.heap) - 1
        self.position[task.task_id] = index
        self._sift_up(index)

    def peek_max(self) -> Task:
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self.heap[0]

    def extract_max(self) -> Task:
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        maximum = self.heap[0]
        last = self.heap.pop()
        del self.position[maximum.task_id]
        if self.heap:
            self.heap[0] = last
            self.position[last.task_id] = 0
            self._sift_down(0)
        return maximum

    def increase_key(self, task_id: str, new_priority: int) -> None:
        if task_id not in self.position:
            raise KeyError(f"Unknown task ID: {task_id}")
        index = self.position[task_id]
        if new_priority < self.heap[index].priority:
            raise ValueError("new_priority must be >= current priority")
        self.heap[index].priority = new_priority
        self._sift_up(index)

    def decrease_key(self, task_id: str, new_priority: int) -> None:
        if task_id not in self.position:
            raise KeyError(f"Unknown task ID: {task_id}")
        index = self.position[task_id]
        if new_priority > self.heap[index].priority:
            raise ValueError("new_priority must be <= current priority")
        self.heap[index].priority = new_priority
        self._sift_down(index)


if __name__ == "__main__":
    pq = MaxPriorityQueue()
    for task in [
        Task("T1", 3, 0, 10),
        Task("T2", 8, 1, 8),
        Task("T3", 5, 2, 12),
        Task("T4", 10, 3, 7),
        Task("T5", 2, 4, 15),
    ]:
        pq.insert(task)

    print("Maximum before update:", pq.peek_max())
    pq.increase_key("T1", 12)
    print("Maximum after T1 priority increase:", pq.peek_max())
    print("Extraction order:")
    while not pq.is_empty():
        print(pq.extract_max())
