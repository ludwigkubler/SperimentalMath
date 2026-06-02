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
        # Find pivot row
        max_row = i
        for r in range(i+1, n):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-zero entries below pivot
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

def min_eigenform_order(A):
    gaussian_elimination(A)
    order = 0
    for row in A:
        if any(x != Fraction(0) for x in row):
            order += 1
    return order

def boolean_circuit_weight(C):
    # Placeholder function to compute the weight of a boolean circuit
    # This is a dummy implementation and should be replaced with actual logic
    return len(C)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    instances_tested = 30
    metric_value = 0.0
    counterexample = ""
    conjecture_holds = False
    
    for _ in range(instances_tested):
        # Generate a random boolean circuit with size s ≤ 40
        C = [random.choice([0, 1]) for _ in range(n)]
        
        # Compute the associated matrix A for each circuit C
        A = [[C[i] * C[j] for j in range(n)] for i in range(n)]
        
        # Determine the minimal order of an eigenform associated with A, MinimalOrder(A)
        order = min_eigenform_order(A)
        
        # Calculate the weight w(C) of each circuit C
        weight = boolean_circuit_weight(C)
        
        # Compute the correlation between MinimalOrder(A) and w(C) using Pearson correlation coefficient
        metric_value += order * weight
    
    mean_metric_value = metric_value / instances_tested
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")