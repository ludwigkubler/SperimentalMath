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

def generate_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        literals = [f"x{i+1}" if i % 2 == 0 else f"~x{i+1}" for i in range(n)]
        random.shuffle(literals)
        clause = " or ".join(literals[:3])
        clauses.append(clause)
    return clauses

def dpll_solve(formula: list) -> bool:
    def solve(model):
        if not formula:
            return True
        literal = next((l for l in formula[0] if l.startswith("x")), None)
        if literal is None:
            return False
        model.add(literal)
        if all(solve(model) for clause in formula if literal in clause):
            return True
        model.remove(literal)
        literal = literal.replace("x", "~x")
        model.add(literal)
        if all(solve(model) for clause in formula if literal in clause):
            return True
        model.remove(literal)
        return False

    model = set()
    return solve(model)

def matrix_representation(formula: list, n: int) -> list:
    matrix = [[0] * (2 * n) for _ in range(2 * n)]
    for clause in formula:
        literals = [l.strip("~") for l in clause.split(" or ")]
        for literal in literals:
            if literal.startswith("x"):
                index = int(literal[1:]) - 1
                matrix[index][index] = 1
            else:
                index = int(literal[2:]) - 1
                matrix[index][index] = -1
    return matrix

def gaussian_elimination(matrix: list) -> list:
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return None
        for j in range(n):
            if i != j and matrix[j][i] != 0:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def minimal_local_system_rank(matrix: list) -> int:
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(n)):
            continue
        rank += 1
        for j in range(n):
            if matrix[j][i] != 0:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    resolution_width = dpll_solve(formula)
    if resolution_width is None:
        return {
            "metric_name": "mls",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_not_computable"
        }
    matrix = matrix_representation(formula, n)
    gaussian_elimination(matrix)
    mls = minimal_local_system_rank(matrix)
    expected_mls = resolution_width ** 2
    return {
        "metric_name": "mls",
        "metric_value": mls,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mls - expected_mls) / expected_mls < 0.1,
        "counterexample": "" if abs(mls - expected_mls) / expected_mls < 0.1 else f"mls={mls}, expected={expected_mls}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ranks = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(mean_ranks)/len(mean_ranks):.2f} std={math.sqrt(sum((x - sum(mean_ranks)/len(mean_ranks))**2 for x in mean_ranks) / len(mean_ranks)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(mean_ranks)/len(mean_ranks):.2f} std={math.sqrt(sum((x - sum(mean_ranks)/len(mean_ranks))**2 for x in mean_ranks) / len(mean_ranks)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mls > 1.1 * resolution_width^2\" first_failing_seed={first_failing_seed}")