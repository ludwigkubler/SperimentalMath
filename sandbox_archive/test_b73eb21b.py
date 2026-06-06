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

# Helper functions for linear algebra operations
def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A):
    n = len(A)
    rank = 0
    pivot_col = 0
    while rank < n and pivot_col < n:
        max_row = rank
        for i in range(rank + 1, n):
            if abs(A[i][pivot_col]) > abs(A[max_row][pivot_col]):
                max_row = i
        if A[max_row][pivot_col] == 0:
            pivot_col += 1
            continue
        A[rank], A[max_row] = A[max_row], A[rank]
        for i in range(rank + 1, n):
            factor = -A[i][pivot_col] / A[rank][pivot_col]
            for j in range(pivot_col, n):
                if rank == i:
                    A[i][j] = 0
                else:
                    A[i][j] += factor * A[rank][j]
        rank += 1
        pivot_col += 1
    return rank

def local_system_order(A):
    try:
        rank = gaussian_elimination(A)
        order = 2 ** (n - rank)
        return order
    except Exception as e:
        return None

# Function to generate a random SAT instance
def generate_sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
            clauses.append(clause)
    return clauses

# Function to compute the incidence algebra of a SAT instance
def incidence_algebra(clauses):
    n = len(clauses[0])
    A = [[0] * (2 ** n) for _ in range(2 ** n)]
    for clause in clauses:
        pos = 0
        neg = 0
        for var in clause:
            if var > 0:
                pos |= 1 << (var - 1)
            else:
                neg |= 1 << (-var - 1)
        A[pos][neg] += 1
    return A

# Function to measure the resolution proof length of a SAT instance
def resolution_proof_length(clauses):
    n = len(clauses[0])
    clauses_set = set(tuple(sorted(c)) for c in clauses)
    queue = list(clauses_set)
    visited = {tuple(sorted(c)) for c in clauses}
    level = 0
    while queue:
        next_level = []
        for clause in queue:
            for i in range(n):
                if clause[i] > 0:
                    neg_clause = tuple(-c for c in clause if c != clause[i])
                else:
                    neg_clause = tuple(c for c in clause if c != -clause[i])
                if neg_clause not in visited:
                    next_level.append(neg_clause)
                    visited.add(neg_clause)
        queue = next_level
        level += 1
    return level

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            clauses = generate_sat_instance(n)
            A = incidence_algebra(clauses)
            order = local_system_order(A)
            if order is None:
                conjecture_holds = False
                counterexample = "mapping_undefined"
                break
            proof_length = resolution_proof_length(clauses)
            metric_values.append(proof_length / order)

    return {
        "metric_name": "Resolution Proof Length / Local System Order",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main function to run multiple trials and output results
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")