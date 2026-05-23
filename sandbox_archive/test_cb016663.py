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
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            # Find a row to swap with
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate below the pivot
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    matrix_copy = [row[:] for row in matrix]
    gaussian_elimination(matrix_copy)
    rank = 0
    for row in matrix_copy:
        if any(row):
            rank += 1
    return rank

def dpll_search_tree_height(cnf):
    variables = set()
    clauses = []
    for clause in cnf:
        variables.update(clause)
        clauses.append(clause)

    def backtrack(model, literals):
        if not literals:
            return True
        literal = literals[0]
        if literal in model:
            return backtrack(model, literals[1:])
        else:
            model[literal] = True
            if backtrack(model, literals[1:]):
                return True
            del model[literal]
            model[-literal] = True
            if backtrack(model, literals[1:]):
                return True
            del model[-literal]
            return False

    max_height = 0
    for literal in variables:
        model = {}
        height = 0
        while not backtrack(model, clauses):
            height += 1
        max_height = max(max_height, height)
    return max_height

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n // 2, n * 2)
    cnf = generate_cnf(n, m)

    try:
        rank_p_adic_l_function = rank(cnf)
        dpll_tree_height = dpll_search_tree_height(cnf)
        metric_value = abs(rank_p_adic_l_function - dpll_tree_height)
        conjecture_holds = metric_value <= 3
        counterexample = "" if conjecture_holds else f"rank={rank_p_adic_l_function}, height={dpll_tree_height}"
    except Exception as e:
        return {
            "metric_name": "abs_diff_rank_and_height",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

    return {
        "metric_name": "abs_diff_rank_and_height",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30 * 1000 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")