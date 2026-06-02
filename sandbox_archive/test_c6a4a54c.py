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

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        # Find pivot
        max_row = i + random.choice(range(rows - i))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i + 1, rows):
            factor = A[j][i] / A[i][i]
            for k in range(cols):
                A[j][k] -= factor * A[i][k]
    
    # Back-substitute to get RREF
    for i in range(rows - 1, -1, -1):
        for j in range(i + 1, rows):
            A[i][-1] -= A[j][-1] * A[i][j]
        A[i][-1] /= A[i][i]
    
    return A

def rank(A):
    rref = gaussian_elimination(A)
    rank = sum(1 for row in rref if any(row))
    return rank

def tropicalize(circuit):
    # Placeholder for tropicalization logic
    # This is a dummy implementation and should be replaced with actual tropicalization code
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = 2  # Degree of the Boolean circuit (d-regular)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * d % 2 != 0:  # Ensure d * n is even
            continue
        
        instances_tested = 0
        thd_sum = 0.0
        wm_sum = 0.0
        n_max = n
        
        for _ in range(30):
            circuit = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            thd_value = rank(tropicalize(circuit))
            wm_value = sum(max(row.count(1), row.count(0)) for row in circuit)
            
            if thd_value is None or wm_value is None:
                continue
            
            instances_tested += 1
            thd_sum += thd_value
            wm_sum += wm_value
        
        if instances_tested == 0:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        thd_avg = thd_sum / instances_tested
        wm_avg = wm_sum / instances_tested
        
        correlation = (instances_tested * sum(thd_value * wm_value for thd_value, wm_value in zip(results, results)) -
                       sum(results) * sum(results)) / math.sqrt((instances_tested * sum(thd_value**2 for thd_value in results) - sum(results)**2) *
                                                            (instances_tested * sum(wm_value**2 for wm_value in results) - sum(results)**2))
        
        results.append(correlation)
    
    if len(results) == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_correlation = sum(results) / len(results)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": mean_correlation,
        "instances_tested": 30 * len(n_values),
        "n_max": n_max,
        "conjecture_holds": mean_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(math.isnan(x) for x in results):
        print("RESULT: INCONCLUSIVE no_valid_data")
    else:
        mean_value = sum(results) / len(results)
        support_fraction = sum(1 for x in results if x >= 0.7) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.7)
            print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation below threshold\" first_failing_seed={first_failing_seed}")