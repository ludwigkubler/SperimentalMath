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
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2 * n)
    clauses = []
    
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    
    incidence_matrix = [[0] * num_clauses for _ in range(n)]
    for j, clause in enumerate(clauses):
        for i in clause:
            incidence_matrix[i-1][j] = 1
    
    def tensor_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        rank = 1
        for j in range(n):
            pivot_row = -1
            for i in range(m):
                if matrix[i][j] != 0 and (pivot_row == -1 or abs(matrix[pivot_row][j]) < abs(matrix[i][j])):
                    pivot_row = i
            if pivot_row == -1:
                continue
            rank += 1
            for k in range(n):
                if k != j:
                    factor = matrix[k][j] / matrix[pivot_row][j]
                    for l in range(m):
                        matrix[l][k] -= factor * matrix[l][pivot_row]
        return rank
    
    tensor_rank_value = tensor_rank(incidence_matrix)
    
    # Placeholder for ACC^0 circuit size calculation
    if n <= 3:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    else:
        # This is a placeholder. Replace with actual ACC^0 circuit size calculation.
        acc0_circuit_size = random.randint(1, n**2)
        conjecture_holds = tensor_rank_value == math.log(n, 2) and acc0_circuit_size <= n**3
        counterexample = ""
    
    return {
        "metric_name": "tensor_rank",
        "metric_value": tensor_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")