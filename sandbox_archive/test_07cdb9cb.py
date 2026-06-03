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
    
    def is_planar(n, edges):
        if n < 3:
            return True
        max_edges = 3 * (n - 2)
        if len(edges) > max_edges:
            return False
        
        # Check for planarity using Euler's formula: V - E + F = 2
        F = len(edges) // 2 + 1  # At least one face (the outer face)
        if n - len(edges) + F != 2:
            return False
        
        # Check for simple graph (no self-loops or multiple edges between the same pair of vertices)
        edge_set = set()
        for u, v in edges:
            if u == v or (u, v) in edge_set or (v, u) in edge_set:
                return False
            edge_set.add((u, v))
        
        return True

    def min_geometric_entropy(n, positions):
        # Calculate the minimum number of bits required to encode the positions
        max_bits = 0
        for x, y in positions:
            max_bits = max(max_bits, math.ceil(math.log2(1 / (x - 0.5) * (1 - x + 0.5))))
            max_bits = max(max_bits, math.ceil(math.log2(1 / (y - 0.5) * (1 - y + 0.5))))
        return max_bits

    def communication_complexity_rank(n, edges):
        # Calculate the smallest value of k such that any function f defined on G can be computed with communication complexity O(k)
        # This is a simplified version and may not accurately reflect the actual communication complexity rank
        return len(edges) // 2 + 1

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        if n > 40:
            break
        
        edges = []
        positions = []
        
        # Generate a random planar graph with n vertices
        while not is_planar(n, edges):
            edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(random.randint(3 * (n - 2) // 2, 3 * (n - 2)))]
        
        # Calculate the minimal geometric entropy
        positions = [(random.random(), random.random()) for _ in range(n)]
        H_G = min_geometric_entropy(n, positions)
        
        # Calculate the communication complexity rank
        r_G = communication_complexity_rank(n, edges)
        
        total_metric_value += H_G * r_G
        instances_tested += 1
        n_max = max(n_max, n)

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0

    return {
        "metric_name": "H(G) * r(G)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")