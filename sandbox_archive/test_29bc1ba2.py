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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(matrix, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        b[i], b[max_row] = b[max_row], b[i]

        factor = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= factor
        b[i] /= factor

        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
                b[j] -= factor * b[i]

    return [b[i] for i in range(n)]

def evaluate_ramanujan_sum(formula, n):
    variables = set()
    for symbol in formula:
        if symbol.startswith('x'):
            variables.add(symbol)
    
    variable_values = {var: random.choice([0, 1]) for var in variables}
    eval_formula = formula
    for var, value in variable_values.items():
        eval_formula = eval_formula.replace(var, str(value))
    
    matrix = []
    b = []
    for i in range(n):
        row = [int(eval_formula)]
        for j in range(1, n):
            row.append(int(eval_formula.replace('x1', str(j))))
        matrix.append(row)
        b.append(i % 2)
    
    try:
        result = gaussian_elimination(matrix, b)
        return len(result)
    except Exception as e:
        print(f"Error evaluating Ramanujan sum: {e}")
        return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    quantifier_depth = random.randint(1, n)
    clause_length = random.randint(1, n)
    
    formula = ''.join(f'x{i+1}' if i < quantifier_depth else f'y{i-quantifier_depth+1}' for i in range(n))
    formula += ' & '.join(f'{random.choice(["~", ""]) + var} -> {random.choice(["~", ""]) + var}' for _ in range(clause_length))
    
    rank_value = evaluate_ramanujan_sum(formula, n)
    
    if rank_value is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = rank_value <= 2 * quantifier_depth
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Rank: {rank_value}, Expected: <= {2 * quantifier_depth}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in res and res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")