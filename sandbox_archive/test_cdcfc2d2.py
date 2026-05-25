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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(n)]

def calculate_minimal_rank(variety_matrix):
    n = len(variety_matrix)
    rank = 0
    for i in range(n):
        if variety_matrix[i][i] == 1:
            rank += 1
            for j in range(i + 1, n):
                if variety_matrix[j][i] == 1:
                    for k in range(n):
                        variety_matrix[j][k] ^= variety_matrix[i][k]
    return rank

def calculate_communication_complexity(n):
    # Simulate the communication complexity for DISJOINTNESS problem
    # This is a simplified version and may not accurately reflect real-world complexities
    return 2 ** (n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bf = generate_boolean_function(n)
        variety_matrix = [[int(bf[i] != bf[j]) for j in range(n)] for i in range(n)]
        min_rank = calculate_minimal_rank(variety_matrix)
        comm_complexity = calculate_communication_complexity(n)
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "comm_complexity": comm_complexity
        })
    
    mean_metric_value = sum(result["min_rank"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["min_rank"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["min_rank"] - result["comm_complexity"]) <= 0.1 * result["min_rank"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")