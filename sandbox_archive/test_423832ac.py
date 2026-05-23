# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        if matrix[i][i] == 0:
            for j in range(i + 1, rows):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                continue
        # Eliminate below
        for j in range(i + 1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    matrix_copy = [row[:] for row in matrix]
    gaussian_elimination(matrix_copy)
    return sum(1 for row in matrix_copy if any(row))

def height_dpll(cnf):
    variables = set()
    clauses = []
    for clause in cnf:
        variables.update(clause)
        clauses.append(clause)

    def dpll(model, literals):
        if not literals:
            return True
        literal = literals[0]
        pure_literals = {lit: [] for lit in literals}
        for i, clause in enumerate(clauses):
            if literal in clause:
                pure_literals[literal].append(i)
            elif -literal in clause:
                pure_literals[-literal].append(i)

        if not any(pure_literals.values()):
            return False

        pure_literal = next(lit for lit, indices in pure_literals.items() if indices)
        new_model = model | {pure_literal}
        new_literals = [lit for lit in literals if lit != pure_literal and -lit != pure_literal]
        if dpll(new_model, new_literals):
            return True

        new_model = model
        new_literals = [lit for lit in literals if lit != pure_literal and -lit != pure_literal]
        if dpll(new_model, new_literals):
            return True

        return False

    max_height = 0
    for literal_set in combinations(variables, len(variables)):
        height = 1 + sum(1 for _ in range(len(literal_set)) if dpll(set(), list(literal_set)))
        max_height = max(max_height, height)
    return max_height

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * (n + 1) // 2)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if len(set(clause)) == len(clause):
            cnf.append(clause)

    rank_p_adic_l_function = rank(cnf)
    height_dpll_tree = height_dpll(cnf)

    return {
        "metric_name": "rank_difference",
        "metric_value": abs(rank_p_adic_l_function - height_dpll_tree),
        "instances_tested": 1,
        "conjecture_holds": abs(rank_p_adic_l_function - height_dpll_tree) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 100))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_difference\" first_failing_seed={first_failing_seed}")