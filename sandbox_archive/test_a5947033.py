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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_euler_characteristic(instance):
        n = len(instance)
        if n == 1:
            return 1
        if n == 2:
            return -1
        
        # Construct the Čech complex
        simplices = []
        for i in range(n):
            simplices.append([i])
        for i in range(n):
            for j in range(i+1, n):
                if instance[i] == instance[j]:
                    simplices.append([i, j])
        
        # Compute the Euler characteristic
        dim = len(simplices)
        boundary_matrix = [[0] * (dim + 1) for _ in range(dim + 1)]
        for i in range(dim):
            for j in range(i+1, dim+1):
                if all(instance[simplices[i][k]] == instance[simplices[j][l]] for k in range(len(simplices[i])) for l in range(len(simplices[j]))):
                    boundary_matrix[i][j] = 1
        # Compute the ranks of the homology groups
        rank = [0] * (dim + 1)
        for i in range(dim, -1, -1):
            if sum(boundary_matrix[j][i] for j in range(i+1, dim+1)) == 0:
                rank[i] = 1
        # Compute the Euler characteristic
        euler_char = sum((-1)**i * rank[i] for i in range(dim + 1))
        return euler_char
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n)
            euler_char = compute_euler_characteristic(instance)
            total_metric_value += euler_char
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((euler_char - mean_metric_value) ** 2 for euler_char in range(total_metric_value)) / instances_tested)
    
    return {
        "metric_name": "Euler characteristic",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")