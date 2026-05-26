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
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    num_clauses = 2 * n
    
    # Generate a random k-CNF instance with n variables and num_clauses clauses
    clauses = []
    for _ in range(num_clauses):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        clauses.append(clause)
    
    # Compute the moment map (simplified version for demonstration purposes)
    A = [[0] * (2 * n) for _ in range(n)]
    for i, clause in enumerate(clauses):
        A[i][abs(clause[0]) - 1] = 1 if clause[0] > 0 else -1
        A[i][abs(clause[1]) - 1 + n] = 1 if clause[1] > 0 else -1
    
    # Compute the rank of the moment map matrix
    rank = gaussian_elimination(A)
    
    # Calculate the expected minimal symplectic leaf rank
    expected_rank = 2 ** (n / 4)
    
    # Check if the conjecture holds for this seed
    conjecture_holds = abs(rank - expected_rank) <= 3
    
    return {
        "metric_name": "minimal_symplectic_leaf_rank",
        "metric_value": rank,
        "instances_tested": num_clauses,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={rank}, expected_rank={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_data")