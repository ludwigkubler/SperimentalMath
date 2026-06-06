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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
        return variables, clauses

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank < m:
                pivot_row = -1
                for j in range(rank, m):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(n):
                    if j != i and matrix[rank][j] != 0:
                        factor = matrix[j][i] / matrix[rank][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank][k]
                rank += 1
        return rank

    def resolution_width(cnf):
        width = 0
        queue = cnf[:]
        while queue:
            clause = queue.pop(0)
            if len(clause) == 1:
                continue
            literal, rest = clause[0], clause[1:]
            new_clauses = []
            for other_clause in queue:
                if literal in other_clause:
                    continue
                if ~literal in other_clause:
                    new_clauses.append([l for l in other_clause if l != ~literal])
                else:
                    new_clauses.append(other_clause)
            width = max(width, len(new_clauses))
            queue.extend(new_clauses)
        return width

    def tropical_divisor_class_group(cnf):
        n = len(cnf[0]) - 1
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            literals = [int(l[1:]) if l.startswith('x') else int(l[2:]) for l in clause]
            for i in literals:
                for j in literals:
                    matrix[i][j] += 1
        return gaussian_elimination(matrix)

    def tseitin_to_cnf(variables, clauses):
        cnf = []
        for clause in clauses:
            cnf.append([f'x{i}' if l.startswith('x') else f'-x{i}' for i, l in enumerate(clause)])
        return cnf

    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = tseitin_formula(n)
    cnf = tseitin_to_cnf(variables, clauses)
    
    rank = tropical_divisor_class_group(cnf)
    width = resolution_width(cnf)
    
    if rank == 0 or width == 0:
        return {
            "metric_name": "rank_over_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    ratio = rank / width
    return {
        "metric_name": "rank_over_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")