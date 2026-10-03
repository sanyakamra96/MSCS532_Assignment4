"""Priority-based scheduler simulation using the custom max-heap queue."""

from priority_queue import MaxPriorityQueue, Task


def run_scheduler(tasks):
    queue = MaxPriorityQueue()
    for task in tasks:
        queue.insert(task)

    schedule = []
    while not queue.is_empty():
        schedule.append(queue.extract_max())
    return schedule


if __name__ == "__main__":
    tasks = [
        Task("T1", priority=3, arrival_time=0, deadline=10),
        Task("T2", priority=8, arrival_time=1, deadline=8),
        Task("T3", priority=5, arrival_time=2, deadline=12),
        Task("T4", priority=10, arrival_time=3, deadline=7),
        Task("T5", priority=2, arrival_time=4, deadline=15),
    ]

    print("Priority-based execution order:")
    for number, task in enumerate(run_scheduler(tasks), start=1):
        print(f"{number}. {task.task_id} (priority={task.priority})")
