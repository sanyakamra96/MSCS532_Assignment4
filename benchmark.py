"""Empirical comparison of Heapsort, Quicksort, and Merge Sort."""

import csv
import random
import time
from pathlib import Path

from heapsort import heapsort


def quicksort(values):
    if len(values) <= 1:
        return values
    pivot = values[random.randrange(len(values))]
    less = [x for x in values if x < pivot]
    equal = [x for x in values if x == pivot]
    greater = [x for x in values if x > pivot]
    return quicksort(less) + equal + quicksort(greater)


def merge_sort(values):
    if len(values) <= 1:
        return values
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def generate_data(size, distribution, seed):
    rng = random.Random(seed)
    base = [rng.randint(0, size * 10) for _ in range(size)]
    if distribution == "sorted":
        return sorted(base)
    if distribution == "reverse-sorted":
        return sorted(base, reverse=True)
    return base


def time_algorithm(name, algorithm, data, repeats=3):
    timings = []
    for _ in range(repeats):
        sample = list(data)
        start = time.perf_counter()
        result = algorithm(sample)
        elapsed = time.perf_counter() - start
        if result is None:
            result = sample
        if result != sorted(data):
            raise AssertionError(f"{name} produced an incorrect result")
        timings.append(elapsed)
    return sum(timings) / len(timings)


def run_benchmark():
    algorithms = {
        "Heapsort": lambda data: heapsort(data),
        "Randomized Quicksort": quicksort,
        "Merge Sort": merge_sort,
    }
    sizes = [1000, 5000, 10000]
    distributions = ["random", "sorted", "reverse-sorted"]
    rows = []

    for distribution in distributions:
        for size in sizes:
            data = generate_data(size, distribution, seed=42 + size)
            for name, algorithm in algorithms.items():
                avg_seconds = time_algorithm(name, algorithm, data)
                rows.append({
                    "distribution": distribution,
                    "size": size,
                    "algorithm": name,
                    "average_seconds": avg_seconds,
                })
                print(f"{distribution:14} n={size:5} {name:20}: {avg_seconds:.6f}s")
    return rows


def save_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def save_chart(rows, path):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; chart generation skipped")
        return

    for distribution in ["random", "sorted", "reverse-sorted"]:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        for algorithm in ["Heapsort", "Randomized Quicksort", "Merge Sort"]:
            subset = [r for r in rows if r["distribution"] == distribution and r["algorithm"] == algorithm]
            subset.sort(key=lambda r: r["size"])
            ax.plot([r["size"] for r in subset], [r["average_seconds"] for r in subset], marker="o", label=algorithm)
        ax.set_title(f"Sorting Performance - {distribution.title()} Input")
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Average Time (seconds)")
        ax.legend()
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        out = path.parent / f"sorting_performance_{distribution}.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)


if __name__ == "__main__":
    results = run_benchmark()
    result_dir = Path(__file__).resolve().parent / "results"
    save_csv(results, result_dir / "benchmark_results.csv")
    save_chart(results, result_dir / "sorting_performance.png")
    print("\nResults written to:", result_dir)
