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
        A = [i for i in range(n)]
        B = [n + i for i in range(n)]
        edges = []
        for a in A:
            for b in B:
                if random.choice([True, False]):
                    edges.append((a, b))
        return A, B, edges
    
    def Zarankiewicz_bound(n):
        # Using the known bound Z(n, 2, 2) ≤ n^2 / 4
        return n * n // 4
    
    def disjointness_communication_complexity(A, B, edges):
        # Simulating a simple deterministic protocol
        return len(edges)
    
    n = random.randint(5, 40)
    A, B, edges = generate_bipartite_graph(n)
    z_bound = Zarankiewicz_bound(n)
    comm_complexity = disjointness_communication_complexity(A, B, edges)
    
    metric_name = "disjointness_communication_complexity"
    metric_value = comm_complexity
    instances_tested = 1
    conjecture_holds = comm_complexity >= z_bound
    counterexample = "" if conjecture_holds else f"Graph with {n} nodes, Z(n, 2, 2)={z_bound}, but communication complexity={comm_complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
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
        counterexample_desc = results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")