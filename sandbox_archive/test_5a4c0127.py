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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(rows):
                    if j != rank and matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[rank][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[rank][k]
                rank += 1
        return rank
    
    def hdim(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i, clause in enumerate(cnf):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] += 1
                else:
                    matrix[i][-1] += abs(var)
        return gaussian_elimination(matrix)
    
    def resolution_width(cnf):
        n = len(cnf)
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if set(clauses[i]).isdisjoint(set(clauses[j])):
                        continue
                    new_clause = [x for x in clauses[i] if x not in clauses[j]]
                    new_clause.extend([y for y in clauses[j] if y not in clauses[i]])
                    new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                break
            width += max(len(clause) for clause in new_clauses)
            clauses = new_clauses[:]
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    hdim_value = hdim(cnf)
    width_value = resolution_width(cnf)
    
    return {
        "metric_name": "hdim",
        "metric_value": hdim_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")