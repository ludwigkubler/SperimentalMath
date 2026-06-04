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

def generate_formula(depth):
    if depth == 0:
        return random.choice(['True', 'False'])
    else:
        op = random.choice(['AND', 'OR'])
        left = generate_formula(depth - 1)
        right = generate_formula(depth - 1)
        return f"({left} {op} {right})"

def incidence_matrix(formula):
    if formula == 'True':
        return [[0]]
    elif formula == 'False':
        return [[1]]
    else:
        op, left, right = formula.split()
        left_matrix = incidence_matrix(left)
        right_matrix = incidence_matrix(right)
        n_left = len(left_matrix)
        n_right = len(right_matrix)
        if op == 'AND':
            return [left_row + right_row for left_row in left_matrix for right_row in right_matrix]
        elif op == 'OR':
            return left_matrix + right_matrix

def gramian_matrix(matrix):
    n = len(matrix)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_product = 0
            for k in range(len(matrix[0])):
                sum_product += matrix[i][k] * matrix[j][k]
            G[i][j] = sum_product
            G[j][i] = sum_product
    return G

def min_symplectic_form_rank(gramian):
    n = len(gramian)
    rank = 0
    for i in range(n):
        pivot = None
        for j in range(i, n):
            if gramian[j][i] != 0:
                pivot = j
                break
        if pivot is None:
            continue
        rank += 1
        for j in range(n):
            if j == i:
                continue
            factor = -gramian[j][i] / gramian[i][i]
            for k in range(n):
                gramian[j][k] += factor * gramian[i][k]
    return rank

def frege_proof_depth(formula):
    if formula == 'True' or formula == 'False':
        return 1
    else:
        op, left, right = formula.split()
        return 2 + max(frege_proof_depth(left), frege_proof_depth(right))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        incidence = incidence_matrix(formula)
        gramian = gramian_matrix(incidence)
        sfr = min_symplectic_form_rank(gramian)
        d = frege_proof_depth(formula)
        results.append((sfr, d))
    
    if len(results) < 30:
        return {
            "metric_name": "symplectic_form_rank_correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    sfr_values = [sfr for sfr, _ in results]
    d_values = [d for _, d in results]
    mean_sfr = sum(sfr_values) / len(sfr_values)
    mean_d = sum(d_values) / len(d_values)
    correlation_coefficient = (sum((sfr - mean_sfr) * (d - mean_d) for sfr, d in results) /
                               math.sqrt(sum((sfr - mean_sfr)**2 for sfr in sfr_values) *
                                         sum((d - mean_d)**2 for d in d_values)))
    
    return {
        "metric_name": "symplectic_form_rank_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")