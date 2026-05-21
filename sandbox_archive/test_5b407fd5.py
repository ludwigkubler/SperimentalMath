# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import product

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if A[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        for j in range(n):
            if j != i and A[rank][j] != 0:
                factor = A[j][i] / A[rank][i]
                for k in range(n):
                    A[j][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def is_linearly_independent(points):
    m, n = len(points), len(points[0])
    A = [points[i] + [-1] for i in range(m)]
    rank = gaussian_elimination(A)
    return rank == n

# Function to generate a random boolean function
def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

# Function to compute the minimal number of generators for the affine plane curve
def min_generators(boolean_function, n):
    points = []
    for x in range(2**n):
        y = boolean_function[x]
        point = [x] + [int(bit) for bit in bin(y)[2:].zfill(n)]
        if not any(all(point[i] == p[i] for i in range(n)) for p in points):
            points.append(point)
    return len(points)

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5  # Start with a small size and increase as needed
    total_generators = 0
    instances_tested = 0

    while True:
        boolean_function = generate_boolean_function(n)
        generators = min_generators(boolean_function, n)
        if generators >= Fraction(2**n, 4):
            total_generators += generators
            instances_tested += 1
        else:
            break
        
        # Increase the size for the next trial
        n += 5

    return {
        "metric_name": "min_generators",
        "metric_value": total_generators / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": total_generators >= Fraction(2**n, 4) * instances_tested,
        "counterexample": ""
    }

# Main function to run multiple trials
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NOT_COMPUTABLE support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not_applicable' first_failing_seed={first_failing_seed}")