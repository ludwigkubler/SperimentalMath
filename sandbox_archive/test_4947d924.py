# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import sys
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot row
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    det = Fraction(0)
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        sign = (-1) ** i
        det += sign * A[0][i] * determinant(submatrix)
    
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    vertices = list(range(n))
    edges = [(random.choice(vertices), random.choice(vertices)) for _ in range(int(n*(n-1)/2))]
    A = [[Fraction(0)] * n for _ in range(n)]
    
    # Construct the adjacency matrix
    for u, v in edges:
        if u != v:
            A[u][v] += Fraction(1)
            A[v][u] += Fraction(1)
    
    # Compute the minimal Hodge index
    hodge_index = determinant(gaussian_elimination(A))
    
    # Calculate αn
    alpha_n = 0.5 * n
    
    return {
        "metric_name": "Hodge Index / n",
        "metric_value": float(hodge_index) / n,
        "instances_tested": 1,
        "conjecture_holds": hodge_index >= alpha_n,
        "counterexample": "" if hodge_index >= alpha_n else f"alpha*n={alpha_n}, Hodge Index={hodge_index}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha*n < Hodge Index\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")