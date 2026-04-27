# auto-injected by SEC sandbox
import itertools
import collections
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
import json

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
            if i != rank and A[i][j] != 0:
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

def cubical_implicant_complex(f, n):
    m = 2**n
    cells = []
    for i in range(m):
        mask = 0
        value = f[i]
        for j in range(n):
            if (i >> j) & 1:
                mask |= 1 << j
        if value == 1:
            cells.append((mask, value))
    return cells

def cubical_boundary_matrix(cells, n):
    m = len(cells)
    boundary_matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if (cells[i][0] & cells[j][0]) == cells[i][0]:
                boundary_matrix[i][j] = 1
    return boundary_matrix

def betti_numbers(boundary_matrix, n):
    m = len(boundary_matrix)
    betti = [0] * (n + 1)
    for k in range(n):
        ker_dim = gaussian_elimination(boundary_matrix[:k+1])
        rank = gaussian_elimination(boundary_matrix[k:])
        betti[k] = ker_dim - rank
    return betti

def dnf_min(f, n):
    m = 2**n
    prime_implicants = []
    for i in range(m):
        if f[i]:
            mask = 0
            value = f[i]
            for j in range(n):
                if (i >> j) & 1:
                    mask |= 1 << j
            prime_implicants.append((mask, value))
    
    def cover(prime_implicants, n):
        covered = [False] * (2**n)
        for implicant in prime_implicants:
            for i in range(2**n):
                if (i & implicant[0]) == implicant[0]:
                    covered[i] = True
        return all(covered)
    
    def backtrack(prime_implicants, n, start=0):
        if cover(prime_implicants[:start], n):
            return 1
        if start >= len(prime_implicants):
            return float('inf')
        min_terms = float('inf')
        for i in range(start, len(prime_implicants)):
            new_prime_implicants = prime_implicants[:i] + prime_implicants[i+1:]
            min_terms = min(min_terms, 1 + backtrack(new_prime_implicants, n, start=i))
        return min_terms
    
    return backtrack(prime_implicants, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 8, 11, 14]:
        f = [random.randint(0, 1) for _ in range(2**n)]
        cells = cubical_implicant_complex(f, n)
        boundary_matrix = cubical_boundary_matrix(cells, n)
        betti = betti_numbers(boundary_matrix, n)
        B_f = sum(betti[k] for k in range(n + 1))
        DNF_min_f = dnf_min(f, n)
        
        if DNF_min_f == float('inf'):
            return {
                "metric_name": "Betti Sum",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        slack = B_f - math.ceil(math.log2(DNF_min_f))
        results.append((n, DNF_min_f, B_f, slack))
    
    total_instances = len(results)
    total_slack = sum(slack for _, _, _, slack in results)
    mean_slack = total_slack / total_instances
    support_fraction = sum(1 for _, _, _, slack in results if slack >= 0) / total_instances
    
    return {
        "metric_name": "Betti Sum",
        "metric_value": mean_slack,
        "instances_tested": total_instances,
        "conjecture_holds": support_fraction >= 0.99,
        "counterexample": "" if support_fraction >= 0.99 else "slack < 0"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_instances = sum(result["instances_tested"] for result in results)
    total_slack = sum(result["metric_value"] * result["instances_tested"] for result in results)
    mean_slack = total_slack / total_instances
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slack < 0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")