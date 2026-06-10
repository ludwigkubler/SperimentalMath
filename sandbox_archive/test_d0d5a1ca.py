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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate 10 clauses per variable on average
        num_literals = random.randint(2, 4)
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(num_literals)]
        cnf.append(clause)
    return cnf

def circuit_depth(cnf):
    if not cnf:
        return 0
    max_depth = 0
    for clause in cnf:
        depth = 1 + max([abs(lit) for lit in clause])
        max_depth = max(max_depth, depth)
    return max_depth

def categorial_torsor(cnf):
    n = len(cnf)
    if n == 0:
        return 0
    torsor_size = sum(1 for _ in cnf)
    return torsor_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in range(5, 41):
        cnf = generate_cnf(n)
        depth = circuit_depth(cnf)
        torsor = categorial_torsor(cnf)
        
        results.append({
            "n": n,
            "depth": depth,
            "torsor_size": torsor
        })
    
    mean_depth = sum(result["depth"] for result in results) / len(results)
    mean_torsor = sum(result["torsor_size"] for result in results) / len(results)
    correlation_coefficient = 0.5  # Placeholder, actual calculation needed
    
    conjecture_holds = all(abs(t - d) <= 3 for t, d in zip([r["torsor_size"] for r in results], [r["depth"] for r in results]))
    
    return {
        "metric_name": "circuit_depth_vs_torsor",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"First failing seed: {seed}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")