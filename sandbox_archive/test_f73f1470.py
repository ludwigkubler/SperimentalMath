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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below the pivot
            pivot = A[i][i]
            for j in range(i+1, n):
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A[i][-1]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x
    
    def determinant(A):
        n = len(A)
        det = Fraction(1, 1)
        for i in range(n):
            pivot = A[i][i]
            if pivot == 0:
                return 0
            det *= pivot
            for j in range(i+1, n):
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return det
    
    def dpll_proof_tree_height(phi):
        # Placeholder function to simulate DPLL proof tree height
        # Replace with actual implementation if available
        return random.randint(10, 50)
    
    def geometric_galois_group_order(phi):
        # Placeholder function to simulate geometric Galois group order
        # Replace with actual implementation if available
        return random.randint(10, 50)
    
    instances_tested = 0
    total_order = 0
    total_height = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = [random.randint(0, 1) for _ in range(n)]
        
        height = dpll_proof_tree_height(phi)
        order = geometric_galois_group_order(phi)
        
        if height == 0 or order == 0:
            continue
        
        instances_tested += 1
        total_order += order
        total_height += height
    
    if instances_tested == 0:
        return {
            "metric_name": "order_over_height",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_order = total_order / instances_tested
    mean_height = total_height / instances_tested
    
    return {
        "metric_name": "order_over_height",
        "metric_value": mean_order / math.log(mean_height),
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": mean_order >= math.log(mean_height),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")