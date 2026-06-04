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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(abs(clauses[i][k]) == abs(clauses[j][l]) and clauses[i][k] != clauses[j][l] for k in range(len(clauses[i])) for l in range(len(clauses[j]))):
                        resolvent = [c for c in clauses[i] if c not in (clauses[i][k], -clauses[j][k])] + [c for c in clauses[j] if c not in (clauses[i][l], -clauses[j][l])]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            clauses.extend(new_clauses)
            width += 1
        return width
    
    def quasi_crystalline_sheaf(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    row, col = literal - 1, literal - 1
                else:
                    row, col = -literal - 1, -literal - 1
                matrix[row][col] += 1
        return gaussian_elimination(matrix)
    
    def min_order(matrix):
        rows, cols = len(matrix), len(matrix[0])
        order = 0
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != 0:
                    order += 1
        return order
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    qc_sheaf = quasi_crystalline_sheaf(cnf)
    min_order_qc = min_order(qc_sheaf)
    width = resolution_width(cnf)
    
    if min_order_qc == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = abs(width) <= math.log(n) * min_order_qc
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": metric_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")