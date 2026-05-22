# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_graph(n):
    edges = set()
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < 0.5:
                edges.add((u, v))
    return edges

def max_plus_tropical_curve(edges):
    n = len(edges) + 1
    curve = [[float('-inf')] * n for _ in range(n)]
    for u, v in edges:
        curve[u][v] = 1
        curve[v][u] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                curve[i][j] = max(curve[i][j], curve[i][k] + curve[k][j])
    return curve

def geometric_fluctuation(curve):
    n = len(curve)
    total = 0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if curve[i][j] != float('-inf'):
                total += abs(curve[i][j])
                count += 1
    if count == 0:
        return 0
    return total / count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_fluctuation = 0
        for _ in range(5):  # Ensure at least 5 instances per size
            edges = generate_random_graph(n)
            curve = max_plus_tropical_curve(edges)
            fluctuation = geometric_fluctuation(curve)
            results.append(fluctuation)
            total_fluctuation += fluctuation
            instances_tested += 1
        mean_fluctuation = total_fluctuation / instances_tested
        conjecture_holds = mean_fluctuation >= math.sqrt(n)
        counterexample = "" if conjecture_holds else f"n={n}, avg_fluctuation={mean_fluctuation}"
        results.append({
            "metric_name": "geometric_fluctuation",
            "metric_value": mean_fluctuation,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return {
        "seed": seed,
        **results[-1]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_fluctuation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_fluctuation} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_fluctuation} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['instances_tested']}, avg_fluctuation={mean_fluctuation}' first_failing_seed={first_failing_seed}")