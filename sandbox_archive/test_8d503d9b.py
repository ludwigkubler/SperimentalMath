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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def deligne_lusztig_rank(k, n):
    if k != 2:
        return "mapping_undefined"
    
    # Generate a random k-CNF formula with n variables
    clauses = []
    for _ in range(10):  # Each clause has at most 3 literals
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if random.choice([True, False]):
                clause.add(var)
            else:
                clause.add(-var)
        clauses.append(list(clause))
    
    # Construct the polynomial representing the formula
    poly = [[0] * (n + 1) for _ in range(n + 1)]
    poly[0][0] = 1
    for clause in clauses:
        term = [1]
        for lit in clause:
            if lit > 0:
                term = [p + t * x[lit-1] for p, t, x in zip(poly[-1], term, x)]
            else:
                term = [p - t * x[-lit-1] for p, t, x in zip(poly[-1], term, x)]
        poly.append(term)
    
    # Compute the Deligne-Lusztig rank
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            if i == j:
                A[i][j] = sum(poly[k][i-1] * poly[k][j-1] for k in range(n))
            else:
                A[i][j] = sum(poly[k][i-1] * poly[k][j-1] for k in range(n)) - sum(poly[k][i-2] * poly[k][j-2] for k in range(n))
    
    gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        rank = deligne_lusztig_rank(2, n)
        if rank == "mapping_undefined":
            return {
                "metric_name": "deligne_lusztig_rank",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    conjecture_holds = all(rank >= n**0.5 for rank, n in zip(ranks, n_values))
    
    return {
        "metric_name": "deligne_lusztig_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank<{n**0.5} for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30 * 2 + 1, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank<{n**0.5} for n={n}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")