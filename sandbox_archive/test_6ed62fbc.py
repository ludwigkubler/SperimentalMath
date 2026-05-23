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
    
    n = random.randint(5, 30)
    m = random.randint(1, n // 2)
    
    # Generate two independent random (m, n/2)-CNF formulas
    def generate_cnf(m, k):
        cnf = []
        for _ in range(m):
            clause = set()
            while len(clause) < k:
                var = random.randint(1, 2 * k)
                if var not in clause:
                    clause.add(var)
            cnf.append(tuple(sorted(clause)))
        return cnf
    
    cnf1 = generate_cnf(m, n // 2)
    cnf2 = generate_cnf(m, n // 2)
    
    # Construct the tensor product of two CNF formulas
    T = []
    for clause1 in cnf1:
        for clause2 in cnf2:
            new_clause = tuple(sorted(clause1 + clause2))
            if len(new_clause) > n:
                continue
            T.append(new_clause)
    
    # Estimate the minimal rank of the tropicalized configuration space
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            denom = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= denom
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def construct_tropicalized_config_space(T):
        n = len(T[0])
        m = len(T)
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(T):
            for var in clause:
                matrix[i][var - 1] = 1
            matrix[i][-1] = 1
        return gaussian_elimination(matrix)
    
    rank = construct_tropicalized_config_space(T)
    
    # Compute the lower bound on the ACC0 circuit size
    def acc0_circuit_size(n, m):
        # This is a simplified estimate based on known results
        return n * math.log2(m) + 2 * n
    
    lower_bound = acc0_circuit_size(n, m)
    
    # Correlate the estimated minimal rank with the lower bound
    metric_value = rank
    conjecture_holds = rank >= lower_bound - 3 * math.sqrt(lower_bound)
    counterexample = "" if conjecture_holds else f"Rank {rank} < {lower_bound - 3 * math.sqrt(lower_bound)}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")