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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph

    def circuit_monotone_width(graph):
        n = len(graph)
        max_width = 0
        for subset_size in range(1, n // 2 + 1):
            subsets = combinations(range(n), subset_size)
            for subset in subsets:
                subgraph = {i: [j for j in graph[i] if j in subset] for i in subset}
                width = len(subset) - len(set.union(*[set(graph[i]) for i in subgraph]))
                max_width = max(max_width, width)
        return max_width

    def integer_lattice_homology(graph):
        n = len(graph)
        homology = [0] * (n + 1)
        homology[0] = 1
        for node in graph:
            neighbors = set(graph[node])
            new_homology = [0] * (n + 1)
            for i in range(n, -1, -1):
                if homology[i] > 0:
                    new_homology[i - len(neighbors)] += homology[i]
                    new_homology[i] -= homology[i]
            homology = new_homology
        return sum(homology)

    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 3)
            homology_rank = integer_lattice_homology(graph)
            width = circuit_monotone_width(graph)
            if homology_rank == 0 or width == 0:
                continue
            correlation_sum += homology_rank * width
            instances_tested += 1

    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean = correlation_sum / instances_tested
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction={support_fraction}")
    else:
        counterexample = min((result["counterexample"] for result in results if result["conjecture_holds"]), default="")
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")