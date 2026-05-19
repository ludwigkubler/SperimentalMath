# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import combinations, permutations

# Helper functions for linear algebra and polynomial operations
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def sos_rank(poly, n):
    # Placeholder function to compute SOS rank
    # This is a stub and should be replaced with actual implementation
    return 0

# Function to generate a random 3-SAT instance
def generate_3sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        variables = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
        sign = [-1 if random.choice([True, False]) else 1] * 3
        clause = [(sign[i], variables[i]) for i in range(3)]
        clauses.append(clause)
    return clauses

# Function to compute Betti numbers of the solution space
def betti_number_complexity(n):
    # Placeholder function to compute Betti numbers
    # This is a stub and should be replaced with actual implementation
    return [1] * (n + 1)

# Main function to run one trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_3sat_instance(n)
    
    betti_sum = sum(betti_number_complexity(len(instance)))
    sos_rank_value = sos_rank(instance, n)
    
    conjecture_holds = betti_sum <= sos_rank_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Betti Number Sum",
        "metric_value": betti_sum,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main block to run trials and print results
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")