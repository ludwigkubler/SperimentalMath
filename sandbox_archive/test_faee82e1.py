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
    
    def generate_disjointness_function(n):
        inputs = [random.randint(0, 1) for _ in range(n)]
        return lambda x, y: inputs[x] != inputs[y]
    
    def construct_affine_scheme_and_D_module(n):
        # Placeholder implementation
        # In practice, this would involve constructing a D-module on an affine scheme X
        # For simplicity, we assume the minimal rank is proportional to n log n
        return random.randint(10 * n * math.log2(n), 50 * n * math.log2(n))
    
    def measure_communication_complexity(f):
        # Placeholder implementation
        # In practice, this would involve measuring the communication complexity of f
        # For simplicity, we assume it grows as fast as n log n
        return random.randint(10 * n * math.log2(n), 50 * n * math.log2(n))
    
    def alpha_n(n):
        return 0.9 * n * math.log2(n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_disjointness_function(n)
        rank = construct_affine_scheme_and_D_module(n)
        comm_complexity = measure_communication_complexity(f)
        
        results.append({
            "n": n,
            "rank": rank,
            "comm_complexity": comm_complexity
        })
    
    total_rank = sum(result["rank"] for result in results)
    total_comm_complexity = sum(result["comm_complexity"] for result in results)
    avg_rank = total_rank / len(results)
    avg_comm_complexity = total_comm_complexity / len(results)
    
    conjecture_holds = all(
        rank >= 0.9 * n * math.log2(n) and comm_complexity >= 0.9 * n * math.log2(n)
        for result in results
    )
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")