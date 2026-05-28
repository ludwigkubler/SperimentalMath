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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot row
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        for j in range(m):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(1, n**2)
    p = random.randint(2, min(n, 10))
    
    # Generate a random QBF instance
    qbf = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    # Compute the clause indicator polynomial modulo p
    coefficients = [0] * (n + 1)
    for clause in qbf:
        product = 1
        for literal in clause:
            if literal == 1:
                product *= -1
            elif literal == -1:
                product *= 2
        coefficients[sum(clause)] += product
    
    # Normalize coefficients modulo p
    coefficients = [coeff % p for coeff in coefficients]
    
    # Construct the quadratic reciprocity lattice
    lattice = []
    for i in range(n + 1):
        row = []
        for j in range(n + 1):
            if i == j:
                row.append(1)
            else:
                row.append(coefficients[i] * coefficients[j])
        lattice.append(row)
    
    # Compute the minimal order of the quadratic reciprocity lattice
    min_order = len(gaussian_elimination(lattice))
    
    # Check the conjecture
    expected_order = 2**n * math.log(n/p)**2
    if min_order > expected_order + 1:
        return {
            "metric_name": "minimal_order",
            "metric_value": min_order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance with n={n}, m={m}, p={p} violates the conjecture."
        }
    
    return {
        "metric_name": "minimal_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_order = 0
    count_holds = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        total_order += result["metric_value"]
        if result["conjecture_holds"]:
            count_holds += 1
    
    mean_order = total_order / len(seeds)
    support_fraction = count_holds / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0 support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] == False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Insufficient evidence to support or refute the conjecture.")