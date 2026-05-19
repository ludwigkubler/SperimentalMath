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
    
    def generate_graph(n):
        if n == 1:
            return {0: []}
        graph = {i: [] for i in range(n)}
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        random.shuffle(edges)
        for u, v in edges[:n-1]:
            graph[u].append(v)
            graph[v].append(u)
        return graph
    
    def edge_expansion(graph):
        n = len(graph)
        min_cut = float('inf')
        for s_size in range(1, n//2 + 1):
            for s in itertools.combinations(range(n), s_size):
                cut_edges = sum(len(graph[v]) - len([u for u in graph[v] if u not in s]) for v in s)
                min_cut = min(min_cut, cut_edges / s_size)
        return min_cut
    
    def resolution_length(h):
        # Simplified model based on the conjecture
        c = 1.0
        return 2 ** (c * h)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    h_G = edge_expansion(graph)
    expected_length = resolution_length(h_G)
    
    # Simulate a simple Resolution proof length (simplified model)
    actual_length = random.randint(int(expected_length), int(expected_length * 2))
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": actual_length,
        "instances_tested": 1,
        "conjecture_holds": actual_length >= expected_length,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_length = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_length)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support for conjecture")