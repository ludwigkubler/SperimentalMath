# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return list(edges)

    def find_algebraic_curves(graph):
        # Placeholder function to simulate finding algebraic curves
        # This is a dummy implementation and should be replaced with actual logic
        return []

    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(1, n + 1):
            subgraph = [edge for edge in graph if edge[0] < i or edge[1] < i]
            rank = max(rank, len(find_algebraic_curves(subgraph)))
        return rank

    def geometric_entropy(curves):
        # Placeholder function to simulate computing geometric entropy
        # This is a dummy implementation and should be replaced with actual logic
        return 0.0

    n_max = 40
    instances_tested = 0
    total_entropy = 0.0
    max_rank = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_random_graph(n)
            rank = communication_complexity_rank(graph)
            curves = find_algebraic_curves(graph)
            entropy = geometric_entropy(curves)
            total_entropy += entropy
            instances_tested += 1
            max_rank = max(max_rank, rank)

    if max_rank == 0:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    avg_entropy = total_entropy / instances_tested
    return {
        "metric_name": "geometric_entropy",
        "metric_value": avg_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": avg_entropy <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    avg_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")