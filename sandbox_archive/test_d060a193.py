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

def generate_formula(n: int) -> str:
    if n == 0:
        return 'True'
    elif n == 1:
        return 'False'
    else:
        op = random.choice(['&', '|'])
        left = generate_formula(random.randint(0, n-1))
        right = generate_formula(random.randint(0, n-1))
        return f'({left} {op} {right})'

def evaluate_formula(formula: str) -> int:
    if formula == 'True':
        return 1
    elif formula == 'False':
        return 0
    else:
        left, op, right = formula.split()
        left_val = evaluate_formula(left)
        right_val = evaluate_formula(right)
        if op == '&':
            return left_val & right_val
        elif op == '|':
            return left_val | right_val

def generate_matroid(formula: str) -> dict:
    n = len(set(c for c in formula if c.isalpha()))
    matroid = {}
    for i in range(n):
        matroid[i] = set()
    for i, c in enumerate(formula):
        if c.isalpha():
            matroid[ord(c) - ord('a')].add(i)
    return matroid

def hodge_index(matroid: dict) -> float:
    rank = len(matroid)
    n = max(len(v) for v in matroid.values())
    index = (rank * (rank + 1)) / (2 * n)
    return index

def communication_matrix(formula: str, n: int) -> list:
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if evaluate_formula(f'({formula[:i]} {chr(97+i)} {formula[i+1:j]} {chr(97+j)})') != evaluate_formula(f'({formula[:i]} {chr(97+i)} {formula[i+1:j]} {chr(97+j-1)})'):
                matrix[i][j] = 1
    return matrix

def rank_variance(matrix: list) -> float:
    n = len(matrix)
    ranks = [sum(row) for row in matrix]
    mean_rank = sum(ranks) / n
    variance = sum((r - mean_rank) ** 2 for r in ranks) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        matroid = generate_matroid(formula)
        h_index = hodge_index(matroid)
        comm_matrix = communication_matrix(formula, n)
        rank_var = rank_variance(comm_matrix)
        results.append((h_index, rank_var))
    metric_name = "Hodge Index vs Rank Variance"
    metric_value = sum(h * r for h, r in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for _, _ in results)
    conjecture_holds = False
    counterexample = ""
    if instances_tested >= 30 and n_max >= 16:
        # Perform linear regression to find correlation coefficient
        x = [h for h, _ in results]
        y = [r for _, r in results]
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        correlation_coefficient = numerator / denominator
        if abs(correlation_coefficient) > 0.7:
            p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(len(x) - 2) / math.sqrt(2)))
            if p_value < 0.05:
                conjecture_holds = True
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")