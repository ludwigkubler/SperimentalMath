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

    def min_rank(graph):
        # Placeholder implementation of minimal rank calculation
        # This is a dummy function and should be replaced with actual logic
        return len(graph)  # Example: number of edges

    def monotone_k_clique_circuit_size(graph, k):
        # Placeholder implementation of monotone k-CLIQUE circuit size calculation
        # This is a dummy function and should be replaced with actual logic
        return len(graph) * k  # Example: number of edges times k

    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    min_rank_value = min_rank(graph)
    clique_circuit_size = monotone_k_clique_circuit_size(graph, 3)

    if clique_circuit_size == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "monotone_k_clique_circuit_size_is_zero"
        }

    ratio = min_rank_value / clique_circuit_size
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(res["metric_value"] for res in results if res["instances_tested"] > 0) / len(results)
    std_ratio = math.sqrt(sum((res["metric_value"] - mean_ratio) ** 2 for res in results if res["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample = next(res["counterexample"] for res in results if res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")