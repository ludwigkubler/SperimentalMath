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
    rank = 0
    for i in range(n):
        if matrix[i][i] == 0:
            j = i + 1
            while j < n and matrix[j][i] == 0:
                j += 1
            if j == n:
                continue
            matrix[i], matrix[j] = matrix[j], matrix[i]
        factor = Fraction(matrix[rank][i], matrix[i][i])
        for k in range(n):
            matrix[j][k] -= factor * matrix[i][k]
        rank += 1
    return rank

def generate_boolean_formula(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    formula = random.choice(literals)
    for _ in range(random.randint(0, n-1)):
        operation = random.choice(['AND', 'OR'])
        other_literal = random.choice(literals)
        if operation == 'AND':
            formula += f' {operation} {other_literal}'
        else:
            formula += f' {operation} ({other_literal})'
    return formula

def count_linear_equations(formula, n):
    matrix = []
    for i in range(n):
        row = [0] * (n + 1)
        row[i] = 1
        matrix.append(row)
    rank = gaussian_elimination(matrix)
    return rank

def frege_proof_depth(formula):
    # Placeholder implementation; actual Frege proof depth calculation is complex
    return len(formula.split())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_equations = 0
    total_depths = 0

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        equations = count_linear_equations(formula, n)
        depth = frege_proof_depth(formula)
        
        total_equations += equations
        total_depths += depth

    mean_equations = total_equations / instances_tested
    mean_depth = total_depths / instances_tested
    
    conjecture_holds = (mean_equations >= math.log(n_max, 2)**2 and 
                         mean_equations <= math.sqrt(n_max) * math.log(n_max))
    
    return {
        "metric_name": "Equations vs Depth",
        "metric_value": mean_depth / math.sqrt(n_max),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")