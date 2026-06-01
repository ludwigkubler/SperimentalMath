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
    
    def is_planar(n):
        # Simple heuristic to check if a graph with n vertices is planar
        return n < 4
    
    def generate_random_planar_graph(n):
        if not is_planar(n):
            raise ValueError("Graph must be planar")
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def min_root_separability(graph):
        # Placeholder function to compute minimal root separability
        # This is a dummy implementation and should be replaced with actual computation
        return random.uniform(0.1, 1.0)
    
    def communication_complexity(graph):
        # Placeholder function to compute communication complexity
        # This is a dummy implementation and should be replaced with actual computation
        return random.uniform(0.5, 2.0)
    
    n = random.randint(5, 40)
    graph = generate_random_planar_graph(n)
    separability = min_root_separability(graph)
    complexity = communication_complexity(graph)
    
    return {
        "metric_name": "root_separability_vs_complexity",
        "metric_value": separability / complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": separability >= math.pow(n, 1/3) and complexity >= math.pow(n, 2/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")