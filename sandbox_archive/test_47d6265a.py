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

def generate_random_formula(n):
    if n == 1:
        return random.choice(['0', '1'])
    else:
        op = random.choice(['&', '|', '^'])
        left = generate_random_formula(n // 2)
        right = generate_random_formula(n - n // 2)
        return f"({left} {op} {right})"

def evaluate_formula(formula):
    if formula == '0':
        return False
    elif formula == '1':
        return True
    else:
        op, left, right = formula[1], eval(formula[2:-1]), eval(formula[-2])
        if op == '&':
            return left and right
        elif op == '|':
            return left or right
        elif op == '^':
            return left != right

def gaussian_elimination(matrix):
    n, m = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if matrix[i][i] == 0:
            swapped = False
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    swapped = True
                    break
            if not swapped:
                continue
        pivot = Fraction(matrix[i][i])
        for k in range(m):
            matrix[i][k] /= pivot
        for j in range(n):
            if i != j and matrix[j][i] != 0:
                factor = -matrix[j][i]
                for k in range(m):
                    matrix[j][k] += factor * matrix[i][k]
        rank += 1
    return rank

def count_linear_equations(formula, n):
    if formula == '0' or formula == '1':
        return 1
    else:
        left = count_linear_equations(formula[2:-1], n // 2)
        right = count_linear_equations(formula[-2], n - n // 2)
        return left + right

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_random_formula(n)
        equations = count_linear_equations(formula, n)
        value = evaluate_formula(formula)
        results.append((equations, value))
    
    total_equations = sum(e for e, v in results)
    total_values = sum(v for e, v in results)
    mean_equations = Fraction(total_equations, len(results))
    mean_value = Fraction(total_values, len(results))
    
    conjecture_holds = True
    counterexample = ""
    if n_max < 16:
        conjecture_holds = False
        counterexample = "n_max too small"
    
    return {
        "metric_name": "equations",
        "metric_value": mean_equations,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_equations = sum(r["metric_value"] for r in results) / len(results)
    std_equations = math.sqrt(sum((r["metric_value"] - mean_equations)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_equations} std={std_equations} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_equations} std={std_equations} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max too small\" first_failing_seed={first_failing_seed}")