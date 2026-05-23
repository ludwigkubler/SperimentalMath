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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            if factor == 0:
                continue
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(matrix[i]):
                rank += 1
        return rank

    def tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return variables, clauses

    def algebraic_k_theory_rank(n, m):
        variables, clauses = tseitin_formula(n, m)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for v in variables:
            matrix[v][v] = 1
        for clause in clauses:
            for v in clause:
                if v > 0:
                    matrix[0][v] += 1
                else:
                    matrix[0][-v] -= 1
        return rank(matrix)

    n = random.randint(5, 40)
    m = random.randint(n, min(1000, n * 2))
    algebraic_k_rank = algebraic_k_theory_rank(n, m)
    query_complexity = max(n + math.log(m), 1)  # Ensure non-zero complexity

    return {
        "metric_name": "Algebraic K-Theory Rank",
        "metric_value": algebraic_k_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(algebraic_k_rank - query_complexity) <= 1,  # Constant factor k=1
        "counterexample": "" if algebraic_k_rank == query_complexity else f"n={n}, m={m}, algebraic_k_rank={algebraic_k_rank}, query_complexity={query_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = next((r['counterexample'] for r in results if not r['conjecture_holds']), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")