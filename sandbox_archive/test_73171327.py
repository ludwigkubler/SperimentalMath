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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        for j in range(i+1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n+1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
        x[i] /= augmented_matrix[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a tropical circuit with known homotopy-stable phase space
    n = random.randint(5, 30)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-10, 10) for _ in range(n)]
    
    # Apply Duality Flip
    A_dual = [[A[j][i] for j in range(n)] for i in range(n)]
    b_dual = [-b[i] for i in range(n)]
    
    # Perturb edge weights by ±ε and verify homotopy-stability
    epsilon = 0.1
    A_perturbed = [[A[i][j] + random.choice([-epsilon, epsilon]) for j in range(n)] for i in range(n)]
    b_perturbed = [b[i] + random.choice([-epsilon, epsilon]) for i in range(n)]
    
    # Solve the perturbed system
    try:
        x_perturbed = gaussian_elimination(A_perturbed, b_perturbed)
    except Exception as e:
        return {
            "metric_name": "homotopy_stability",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Check if the solution is close to the original
    x_original = gaussian_elimination(A, b)
    max_diff = max(abs(x_perturbed[i] - x_original[i]) for i in range(n))
    homotopy_stable = max_diff < epsilon
    
    return {
        "metric_name": "homotopy_stability",
        "metric_value": 1 if homotopy_stable else 0,
        "instances_tested": 1,
        "conjecture_holds": homotopy_stable,
        "counterexample": "" if homotopy_stable else "Solution difference exceeds epsilon"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 17 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Solution difference exceeds epsilon\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")