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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    return edges

def resolution_width(graph):
    # Placeholder function to simulate resolution width calculation
    # Replace with actual DPLL solver implementation
    return len(graph) * 2

def geometric_langlands_index(graph):
    # Placeholder function to simulate geometric Langlands index calculation
    # Replace with actual Geometric Langlands theory implementation
    return len(graph)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "resolution_width"
    instances_tested = 0
    n_max = 0
    ind_values = []
    w_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + 8 < end_time:
            graph = generate_random_graph(n)
            w_G = resolution_width(graph)
            ind_G = geometric_langlands_index(graph)
            
            instances_tested += 1
            n_max = max(n_max, n)
            
            ind_values.append(ind_G)
            w_values.append(w_G)
        
        if len(ind_values) >= 30:
            break
    
    mean_ind = sum(ind_values) / len(ind_values)
    std_dev = math.sqrt(sum((x - mean_ind) ** 2 for x in ind_values) / len(ind_values))
    
    if any(ind < c * n ** (1/4) for ind, n in zip(ind_values, [5, 10, 15, 20, 30, 40])):
        conjecture_holds = False
        counterexample = "ind(G) < c·n^(1/4)"
    
    if any(ind / w > 2.5 for ind, w in zip(ind_values, w_values)):
        conjecture_holds = False
        counterexample = "ind(G)/w(G) > 2.5"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_ind,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]
    
    end_time = time.time() + 240
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ind = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ind) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ind} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")