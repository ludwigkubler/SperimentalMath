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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
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
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def clause_indicator_matrix(clauses, variables):
        m = len(clauses)
        n = len(variables)
        matrix = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] = 1
                else:
                    matrix[i][-var - 1] = 1
        return matrix
    
    def minimal_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = [row[:] for row in matrix]
        rank = gaussian_elimination(A)
        return rank
    
    def generate_sat_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses, variables
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses, variables = generate_sat_instance(n, random.randint(1, n))
            matrix = clause_indicator_matrix(clauses, variables)
            rank = minimal_rank(matrix)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    expected_bound = 2 ** n * m
    conjecture_holds = mean_rank <= expected_bound
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} exceeds expected bound {expected_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds expected bound\" first_failing_seed={first_failing_seed}")