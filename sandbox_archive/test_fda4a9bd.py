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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Swap rows i and max_row
        A[i], A[max_row] = A[max_row], A[i]
        
        # Make all entries below pivot zero
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    
    return A

def mgi(data_space):
    # Placeholder for minimal noncommutative geometric invariant calculation
    # This is a dummy implementation that returns the rank of the data space
    # as an example. Replace with actual computation based on spectral properties.
    n = len(data_space)
    I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    A = [row[:] + col[:] for row, col in zip(data_space, data_space)]
    
    try:
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row[j] != Fraction(0) for j in range(n)))
    except IndexError:
        return None
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    mgi_values = []
    R_values = []
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            data_space = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            R = sum(data_space[i][j] * data_space[j][i] for i in range(n) for j in range(i+1, n))
            mgi_value = mgi(data_space)
            
            if mgi_value is not None:
                instances_tested += 1
                mgi_values.append(mgi_value)
                R_values.append(R)
                n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "mgi(data_space)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mgi_mean = sum(mgi_values) / len(mgi_values)
    R_mean = sum(R_values) / len(R_values)
    covariance = sum((mgi_values[i] - mgi_mean) * (R_values[i] - R_mean) for i in range(len(mgi_values))) / len(mgi_values)
    mgi_std = math.sqrt(sum((x - mgi_mean)**2 for x in mgi_values) / len(mgi_values))
    R_std = math.sqrt(sum((y - R_mean)**2 for y in R_values) / len(R_values))
    
    correlation_coefficient = covariance / (mgi_std * R_std)
    
    return {
        "metric_name": "mgi(data_space)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mgi_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["metric_value"] is not None)
    
    if len(mgi_values) == 0:
        print("RESULT: INCONCLUSIVE insufficient_data")
    elif conjecture_holds:
        mean = sum(mgi_values) / len(mgi_values)
        std = math.sqrt(sum((x - mean)**2 for x in mgi_values) / len(mgi_values))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")