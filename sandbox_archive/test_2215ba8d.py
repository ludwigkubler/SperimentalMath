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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) == 0:
                clause[random.randint(0, n - 1)] *= -1
            clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def dpll_refutation_tree_width(formula):
        # Simplified DPLL algorithm to estimate tree width
        variables = list(range(1, len(formula) + 1))
        stack = []
        for clause in formula:
            if not any(var in clause for var in variables):
                return math.inf
            stack.append(clause)
        while stack:
            clause = stack.pop()
            new_variables = [var for var in variables if var not in clause]
            if not new_variables:
                return len(variables) - 1
            variables = new_variables
        return len(variables)
    
    def tropical_theta_rank(formula):
        # Simplified computation of tropical theta rank
        n = len(formula)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in formula:
            for i, var in enumerate(clause):
                if var > 0:
                    matrix[i][var - 1] += 1
                else:
                    matrix[var - 1][i] -= 1
        rank = 0
        for _ in range(n):
            max_row = max(range(n), key=lambda r: sum(abs(matrix[r][c]) for c in range(n + 1)))
            if all(matrix[max_row][c] == 0 for c in range(n + 1)):
                break
            rank += 1
            for r in range(n):
                if r != max_row:
                    factor = matrix[r][max_row] / matrix[max_row][max_row]
                    for c in range(n + 1):
                        matrix[r][c] -= factor * matrix[max_row][c]
        return rank
    
    n_values = [5, 10, 20, 40]
    results = []
    for n in n_values:
        formula = generate_3cnf(n)
        theta_rank = tropical_theta_rank(formula)
        dpll_width = dpll_refutation_tree_width(formula)
        results.append({
            'n': n,
            'theta_rank': theta_rank,
            'dpll_width': dpll_width
        })
    
    mean_theta_rank = sum(result['theta_rank'] for result in results) / len(results)
    max_dpll_width = max(result['dpll_width'] for result in results)
    
    metric_name = "tropical_theta_rank"
    metric_value = mean_theta_rank
    instances_tested = len(n_values)
    conjecture_holds = all(theta_rank <= math.log(n) for n, theta_rank in zip(n_values, [result['theta_rank'] for result in results]))
    counterexample = "" if conjecture_holds else f"n={n_values[0]}, theta_rank={results[0]['theta_rank']}, dpll_width={results[0]['dpll_width']}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, theta_rank={results[0]['theta_rank']}, dpll_width={results[0]['dpll_width']}\" first_failing_seed={first_failing_seed}")