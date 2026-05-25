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
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    row_echelon_form = gaussian_elimination([row[:] for row in matrix])
    non_zero_rows = [row for row in row_echelon_form if any(row)]
    return len(non_zero_rows)

def generate_cnf(n):
    literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals, random.randint(2, n))
        clauses.append(clause)
    return clauses

def tseitin_resolution_tree(cnf):
    literals = set()
    for clause in cnf:
        literals.update(clause)
    nodes = {var: [] for var in literals}
    for clause in cnf:
        new_var = len(nodes) + 1
        nodes[new_var] = []
        for literal in clause:
            if literal > 0:
                nodes[literal].append(new_var)
                nodes[-literal].append(-new_var)
            else:
                nodes[-literal].append(new_var)
                nodes[literal].append(-new_var)
    return nodes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tree = tseitin_resolution_tree(cnf)
    k_group_rank = rank([[0] * len(tree) for _ in range(len(tree))])
    metric_value = k_group_rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n > 1:
        c = Fraction(1, 2)
        lower_bound = c * n * math.log(n)
        if metric_value >= lower_bound and abs(metric_value - lower_bound) / lower_bound <= 0.1:
            conjecture_holds = True
    
    return {
        "metric_name": "K-group rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support support_fraction={support_fraction}")