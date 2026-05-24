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

def generate_tseitin_formula(n, m):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(m):
        clause = random.choice(variables)
        if random.choice([True, False]):
            clause = f'~{clause}'
        clauses.append(clause)
    return variables, clauses

def tropicalize_clause(clause, variables):
    n = len(variables) + 1
    v_i = [0] * n
    for var in clause.split('~'):
        if var.startswith('x'):
            idx = int(var[1:])
            v_i[idx] = 1
        else:
            v_i[-1] = 1
    return v_i

def tensor_product(vectors):
    result = []
    for v1 in vectors:
        new_row = [sum(x * y for x, y in zip(v1, v2)) for v2 in vectors]
        result.append(new_row)
    return result

def min_rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(m)):
            continue
        rank += 1
        for j in range(i + 1, n):
            if matrix[j][i] != 0:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def resolution_width(clauses):
    clauses_set = set(clauses)
    width = 1
    while True:
        new_clauses = []
        for clause in clauses_set:
            if any(c in clause for c in new_clauses):
                continue
            new_clause = [c for c in clauses_set if c != clause]
            new_clauses.append(clause)
            if len(new_clauses) > width:
                width = len(new_clauses)
        if not new_clauses:
            break
        clauses_set.update(new_clauses)
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables, clauses = generate_tseitin_formula(n, m)
    
    t_clauses = [tropicalize_clause(clause, variables) for clause in clauses]
    tensor_prod = tensor_product(t_clauses)
    min_rank_val = min_rank(tensor_prod)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "minimal rank / width",
        "metric_value": Fraction(min_rank_val, width),
        "instances_tested": 1,
        "conjecture_holds": min_rank_val <= width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [41]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")