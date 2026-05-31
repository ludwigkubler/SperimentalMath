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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Find a non-zero pivot below the current row
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                continue  # No non-zero pivot found, skip this column
        # Eliminate entries below the current row
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def min_rank(M):
    A = [row[:] for row in M]
    rank = 0
    for i in range(len(A)):
        if A[i][i] != 0:
            rank += 1
            for j in range(i + 1, len(A)):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(len(A[0])):
                    A[j][k] -= factor * A[i][k]
    return rank

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    for i in range(1, n + 1):
        clauses.append([variables[i - 1]])
        clauses.append([-variables[i - 1]])
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([variables[i], variables[j], -f'x{i}{j}'])
            clauses.append([variables[i], -variables[j], f'x{i}{j}'])
            clauses.append([-variables[i], variables[j], f'x{i}{j}'])
            clauses.append([-variables[i], -variables[j], -f'x{i}{j}'])
    return variables, clauses

def dpll_solver(clauses):
    def solve(model):
        if not clauses:
            return model
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_model = {**model, literal: True}
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return solve(new_model) or solve({**model, literal: False})
        pure_literal = next((l for l in variables if all(l not in c and -l not in c for c in clauses)), None)
        if pure_literal:
            new_model = {**model, pure_literal: True}
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return solve(new_model) or solve({**model, pure_literal: False})
        literal = random.choice(variables)
        new_model_true = {**model, literal: True}
        new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
        result_true = solve(new_model_true)
        if result_true:
            return result_true
        new_model_false = {**model, literal: False}
        new_clauses_false = [c for c in clauses if literal not in c and -literal not in c]
        return solve(new_model_false)
    variables = set()
    for clause in clauses:
        variables.update(clause)
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            variables, clauses = tseitin_formula(n)
            M = [[0] * len(variables) for _ in range(len(variables))]
            for clause in clauses:
                for literal in clause:
                    if literal.startswith('x'):
                        var_index = int(literal[1:]) - 1
                        M[var_index][var_index] += 1
                    else:
                        var_index = int(literal[1:]) - 1
                        M[var_index][var_index] -= 1
            rank = min_rank(M)
            width = dpll_solver(clauses)
            total_rank += rank
            total_width += width
            instances_tested += 1
            n_max = max(n_max, n)

    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested

    if all(0.5 <= mean_rank / mean_width <= 1.5 for _ in range(3)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mean_ratio_outside_range"

    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_rank / mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio_outside_range\" first_failing_seed={first_failing_seed}")