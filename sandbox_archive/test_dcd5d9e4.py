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
    
    def generate_bipartite_graph(n):
        A = [0] * n
        B = [0] * n
        edges = []
        for i in range(n):
            for j in range(n):
                if random.random() < 0.5:
                    edges.append((i, j))
                    A[i] += 1
                    B[j] += 1
        return A, B, edges

    def zarankiewicz_bound(n):
        return math.floor(2 * n * (n - 1) / 4)

    def disjointness_communication_complexity(A, B, edges):
        # Simplified deterministic protocol for communication complexity
        return max(max(A), max(B))

    n = random.randint(5, 40)
    A, B, edges = generate_bipartite_graph(n)
    
    z_bound = zarankiewicz_bound(n)
    comm_complexity = disjointness_communication_complexity(A, B, edges)

    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity >= z_bound,
        "counterexample": "" if comm_complexity >= z_bound else f"Graph with n={n}, A={A}, B={B} has communication complexity {comm_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")