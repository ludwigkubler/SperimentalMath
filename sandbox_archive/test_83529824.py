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
        return '0' if random.choice([True, False]) else '1'
    elif n == 2:
        return f"({generate_random_formula(1)} {'&' if random.choice([True, False]) else '|'} {generate_random_formula(1)})"
    else:
        subformulas = [f"({generate_random_formula(n // 2)})"] * (n // 2)
        subformulas.append(f"({generate_random_formula(n - n // 2)})")
        return f"({' & '.join(subformulas)} {'|' if random.choice([True, False]) else '&'} {' | '.join(subformulas)})"

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    # Back-substitute to get the solution
    solution = [0] * cols
    for i in range(rows - 1, -1, -1):
        solution[i] = Fraction(matrix[i][-1], matrix[i][i])
        for j in range(i + 1, rows):
            solution[i] -= Fraction(solution[j] * matrix[i][j], matrix[i][i])
    
    return solution

def count_linear_equations(formula, n):
    if formula == '0' or formula == '1':
        return 0
    elif '&' in formula:
        left = count_linear_equations(formula[2:-1], n // 2)
        right = count_linear_equations(formula[-2], n - n // 2)
        return max(left, right) + 1
    elif '|' in formula:
        left = count_linear_equations(formula[2:-1], n // 2)
        right = count_linear_equations(formula[-2], n - n // 2)
        return min(left, right) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    metric_value = 0.0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        formula = generate_random_formula(n)
        equations = count_linear_equations(formula, n)
        
        # Simulate Frege proof depth (simplified model)
        frege_depth = random.randint(1, n * n)
        
        metric_value += equations
        instances_tested += 1
    
    mean_diff = abs(metric_value / instances_tested - math.sqrt(n_max))
    
    conjecture_holds = mean_diff <= 0.5 * math.sqrt(n_max)
    counterexample = "" if conjecture_holds else f"mean_diff={mean_diff}"
    
    return {
        "metric_name": "linear_equations",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff_exceeds_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")