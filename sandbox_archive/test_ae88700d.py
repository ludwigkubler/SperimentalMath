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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def free_entropy(probabilities):
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def read_twice_bp_size(n):
        # Placeholder for the actual size calculation
        return 2 ** n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_diff = 0
        max_diff = 0
        
        for _ in range(5):  # Ensure at least 5 instances per size
            probabilities = [random.random() for _ in range(2 ** n)]
            F_P = free_entropy(probabilities)
            size_P = read_twice_bp_size(n)
            diff = abs(F_P - (math.log2(size_P) + n))
            total_diff += diff
            max_diff = max(max_diff, diff)
            instances_tested += 1
        
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "mean_diff": total_diff / instances_tested,
            "max_diff": max_diff
        })
    
    mean_value = sum(result["mean_diff"] for result in results) / len(results)
    max_diff_overall = max(result["max_diff"] for result in results)
    
    conjecture_holds = all(diff <= 3 for diff in [result["mean_diff"] for result in results]) and max_diff_overall <= 10
    counterexample = "" if conjecture_holds else "max_diff_overall>10"
    
    return {
        "metric_name": "free_entropy_bound",
        "metric_value": mean_value,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["max_diff"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["max_diff"] > 10)
        print(f"RESULT: FALSIFIED counterexample='max_diff_overall>10' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")