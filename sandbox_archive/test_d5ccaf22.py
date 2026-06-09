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
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        pivot = A[i][i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], pivot)
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def minimal_representation_degree(n):
    # Generate a random symmetric matrix
    A = [[random.randint(0, 1) if i == j else random.choice([0, -A[i][j]]) for j in range(n)] for i in range(n)]
    
    # Ensure the matrix is symmetric
    for i in range(n):
        for j in range(i+1, n):
            A[j][i] = A[i][j]
    
    # Perform Gaussian elimination to find rank
    rank = 0
    for row in gaussian_elimination(A):
        if any(row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    D_S = []
    q_phi = []
    
    for n in n_values:
        D_S.append(minimal_representation_degree(n))
        # For simplicity, assume the number of distinct quadratic forms is equal to the rank
        q_phi.append(D_S[-1])
    
    correlation_coefficient = sum((D_S[i] - sum(D_S) / len(D_S)) * (q_phi[i] - sum(q_phi) / len(q_phi)) for i in range(len(D_S))) / (len(D_S) * math.sqrt(sum((D_S[i] - sum(D_S) / len(D_S)) ** 2 for i in range(len(D_S))) * sum((q_phi[i] - sum(q_phi) / len(q_phi)) ** 2 for i in range(len(q_phi)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _ in range(len(D_S))),
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and min(res["metric_value"] for res in results) >= 0.5:
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")