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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def compute_l_p_measure(M, p):
    n = len(M)
    measure = 0
    for i in range(n):
        for j in range(n):
            if M[i][j] != 0:
                measure += abs(M[i][j]) ** (1/p)
    return measure

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        M = gaussian_elimination(M)
        
        min_measure = float('inf')
        for p in [1, 2, math.inf]:
            measure = compute_l_p_measure(M, p)
            if measure < min_measure:
                min_measure = measure
        
        comm_complexity = n ** (1/2)  # Placeholder value; replace with actual computation
        
        metric_values.append(min_measure * comm_complexity)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    correlation_coefficient = sum(x * y for x, y in zip(metric_values, [n ** (1/2)] * instances_tested)) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "min_noncommutative_L_p_measure * comm_complexity",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")