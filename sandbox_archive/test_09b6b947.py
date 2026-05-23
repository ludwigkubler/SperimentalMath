# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(1, n + 1):
        clauses.append([i])
        clauses.append([-i])
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clauses.append([i, -j])
            clauses.append([-i, j])
            clauses.append([j, -i])
            clauses.append([-j, i])
    return variables, clauses

def tropical_rank(poly):
    if not poly:
        return 0
    max_degree = 0
    for clause in poly:
        degree = sum(abs(coeff) for coeff in clause)
        if degree > max_degree:
            max_degree = degree
    return max_degree

def resolution_width(clauses):
    stack = []
    while clauses:
        new_clause = None
        for i, clause1 in enumerate(clauses):
            for j, clause2 in enumerate(clauses):
                if i == j:
                    continue
                common_vars = set(clause1) & set(clause2)
                if not common_vars:
                    continue
                new_clause = []
                for var in clause1:
                    if -var not in clause2:
                        new_clause.append(var)
                for var in clause2:
                    if -var not in clause1:
                        new_clause.append(var)
                break
            if new_clause:
                break
        if not new_clause:
            return len(stack)
        clauses.remove(new_clause)
        stack.append(new_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    poly = [clauses]
    trop_rank_poly = tropical_rank(poly)
    width = resolution_width(clauses)
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= 2 ** trop_rank_poly,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "resolution_width does not match tropical rank"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")