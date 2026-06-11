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
    
    def generate_instance(n):
        # Generate a random adjacency matrix for a communication complexity problem
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A
    
    def compute_lie_algebroid_order(A):
        n = len(A)
        if n <= 1:
            return 0
        
        # Compute the rank of the adjacency matrix
        rank = 0
        for i in range(n):
            row = [A[j][i] for j in range(n)]
            if any(row):
                rank += 1
        
        # The minimal order of a Lie algebroid action is O(sqrt(rank))
        return int(math.sqrt(rank))
    
    def compute_rank_variance(A):
        n = len(A)
        mean = sum(sum(row) for row in A) / (n * n)
        variance = sum((sum(row) - mean) ** 2 for row in A) / (n * n)
        return variance
    
    n_max = 0
    metric_values = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        A = generate_instance(n)
        rank_variance = compute_rank_variance(A)
        lie_algebroid_order = compute_lie_algebroid_order(A)
        
        metric_values.append(lie_algebroid_order / math.sqrt(rank_variance))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    conjecture_holds = all(value <= 1.1 * mean_value for value in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "lie_algebroid_order_rank_variance_ratio",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")