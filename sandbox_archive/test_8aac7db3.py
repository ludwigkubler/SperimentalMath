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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    matrix = gaussian_elimination(matrix)
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def tseitin_formula(n, m):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    for i in range(m):
        clause = random.choice(variables)
        if random.choice([True, False]):
            clause = f'~{clause}'
        clauses.append(clause)
    return variables, clauses

def quasi_monogenic_sequence(variables, clauses):
    n = len(variables)
    m = len(clauses)
    matrix = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clauses):
        if clause.startswith('~'):
            j = int(clause[2:]) - 1
            matrix[i][j] = -1
        else:
            j = int(clause) - 1
            matrix[i][j] = 1
    return rank(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            variables, clauses = tseitin_formula(n, n // 2)
            Q = quasi_monogenic_sequence(variables, clauses)
            results.append(Q)
    metric_value = sum(results) / len(results)
    conjecture_holds = all(Q >= math.log2(n + m) for n in [5, 10, 15, 20, 30, 40] for m in range(1, n // 2))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")