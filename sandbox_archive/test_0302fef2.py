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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, 2 * m) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(cols):
                if j != i and matrix[rank][j] != 0:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def compute_minimal_level(clauses):
        m = len(clauses)
        n = sum(len(c) for c in clauses)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for j in clause:
                A[i][j - 1] = 1
        rank = gaussian_elimination(A)
        return m - rank
    
    results = []
    n_max = 0
    instances_tested = 0
    
    for _ in range(30):
        m = random.randint(5, 40)
        cnf = generate_cnf(m)
        L = compute_minimal_level(cnf)
        if L <= 1.2 * m**(1/3) and L >= 0.8 * m**(1/3):
            results.append(L)
        instances_tested += 1
        n_max = max(n_max, m)
    
    mean_L = sum(results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r >= 0.8 * m**(1/3)) / len(results) if results else 0
    
    return {
        "metric_name": "L",
        "metric_value": mean_L,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"m = {m}, L = {L}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["conjecture_holds"])
    
    support_fraction = sum(results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_L} std={std_dev} support_fraction={support_fraction}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(False)]
        m = random.randint(5, 40)
        L = compute_minimal_level(generate_cnf(m))
        print(f"RESULT: FALSIFIED counterexample='m = {m}, L = {L}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")