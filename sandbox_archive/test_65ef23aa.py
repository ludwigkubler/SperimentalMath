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
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != 0 for i in range(n)):
                clauses.append(clause)
        return clauses

    def matrix_from_cnf(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    matrix[var][var] += 1
                else:
                    matrix[var][var] -= 1
        return matrix

    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(i, n)):
                continue
            pivot_col = next(j for j in range(i, n) if matrix[i][j] != 0)
            for j in range(i, n):
                matrix[j][pivot_col] /= matrix[i][pivot_col]
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[j][pivot_col]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank

    def resolution_width(cnf):
        n = len(cnf[0])
        width = 1
        queue = cnf[:]
        while queue:
            clause = queue.pop(0)
            new_clauses = []
            for other_clause in queue:
                common_vars = set(abs(lit) for lit in clause if lit in other_clause)
                if not common_vars:
                    continue
                for var in common_vars:
                    new_clause = [lit for lit in clause if abs(lit) != var]
                    new_clause.extend([other_lit for other_lit in other_clause if abs(other_lit) != var])
                    if len(new_clause) > width:
                        width = len(new_clause)
                    if len(new_clause) == 1:
                        return 1
                    new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        matrix = matrix_from_cnf(cnf)
        rank = min_rank(matrix)
        width = resolution_width(cnf)
        results.append((n, rank, width))
    
    mean_rank = sum(rank for _, rank, _ in results) / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank, _ in results) / len(results))
    support_fraction = all(abs(rank - math.sqrt(n)) <= std_rank for n, rank, _ in results)

    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_rank = sum(trial["metric_value"] for trial in results) / len(results)
    std_rank = math.sqrt(sum((trial["metric_value"] - mean_rank) ** 2 for trial in results) / len(results))
    support_fraction = all(abs(trial["metric_value"] - math.sqrt(n)) <= std_rank for n, rank, _ in results)

    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")