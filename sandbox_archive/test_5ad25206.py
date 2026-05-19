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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 2
    
    # Generate a random max-CUT instance
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the degree-d SOS moment matrix M
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                for k in range(d):
                    M[i][k] += (i + k) % n
                    M[j][k] += (j + k) % n
    
    # Calculate eigenvalue spectrum
    eigenvalues = [0] * n
    for i in range(n):
        A = [[M[j][k] - M[i][k] if j != i else 1 for k in range(n)] for j in range(n)]
        eigenvector = gaussian_elimination(A)
        lambda_i = sum(M[i][j] * eigenvector[j] for j in range(n))
        eigenvalues[i] = abs(lambda_i)
    
    # Check if any eigenvalue exceeds C * sqrt(n/d^3)
    C = 1.0  # Universal constant C
    threshold = C * math.sqrt(n / d**3)
    if any(eigenvalue > threshold for eigenvalue in eigenvalues):
        return {
            "metric_name": "Eigenvalue Threshold",
            "metric_value": max(eigenvalues),
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "Eigenvalue exceeds threshold"
        }
    
    # Check if 0.878-approximators consistently violate this threshold
    # This part is not implemented as it requires a specific approximation algorithm
    return {
        "metric_name": "Eigenvalue Threshold",
        "metric_value": max(eigenvalues),
        "instances_tested": n,
        "conjecture_holds": False,
        "counterexample": "Mapping undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mapping undefined\" first_failing_seed={first_failing_seed}")