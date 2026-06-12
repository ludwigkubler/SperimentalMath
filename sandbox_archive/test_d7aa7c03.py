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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def configuration_space(edges):
        return len(edges)
    
    def depth_complexity(n):
        # Simplified model for circuit depth complexity
        return n * (n - 1) // 2
    
    def correlation_coefficient(r_values, d_values):
        if not r_values or not d_values:
            return 0.0
        mean_r = sum(r_values) / len(r_values)
        mean_d = sum(d_values) / len(d_values)
        numerator = sum((r - mean_r) * (d - mean_d) for r, d in zip(r_values, d_values))
        denominator = math.sqrt(sum((r - mean_r) ** 2 for r in r_values)) * math.sqrt(sum((d - mean_d) ** 2 for d in d_values))
        return numerator / denominator if denominator != 0 else 0.0
    
    n_max = 40
    instances_tested = 30
    r_values = []
    d_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        G_edges = generate_graph(n)
        r_G = configuration_space(G_edges)
        d_C = depth_complexity(n)
        r_values.append(r_G)
        d_values.append(d_C)
    
    correlation = correlation_coefficient(r_values, d_values)
    conjecture_holds = correlation >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation {correlation} < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")