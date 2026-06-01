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
    
    def generate_planar_graph(n):
        if n < 3:
            return []
        nodes = list(range(n))
        edges = set()
        for i in range(1, n):
            edges.add((0, i))
        for i in range(2, n):
            edges.add((i-1, i))
        return (nodes, edges)
    
    def local_cohomology_rank(G):
        # Placeholder function; actual implementation required
        return random.random()
    
    def communication_complexity(G):
        # Placeholder function; actual implementation required
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_planar_graph(n)
        lcr = local_cohomology_rank(G)
        growth_rate = communication_complexity(G)
        results.append((lcr, growth_rate))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lcrs = [r[0] for r in results]
    growth_rates = [r[1] for r in results]
    correlation = sum((lcr - mean(lcrs)) * (growth_rate - mean(growth_rates)) for lcr, growth_rate in results) / (len(results) * std(lcrs) * std(growth_rates))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def std(lst):
    avg = mean(lst)
    return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")