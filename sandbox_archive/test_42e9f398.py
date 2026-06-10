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
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i + 1, n):
                clauses.append([f'-{literals[i]}', f'{literals[j]}'])
                clauses.append([f'-{literals[j]}', f'{literals[i]}'])
        return literals, clauses
    
    def evaluate_quadratic_form(literals, clauses, x):
        value = 0
        for clause in clauses:
            term = 1
            for lit in clause:
                if lit.startswith('-'):
                    term *= (x[int(lit[1:]) - 1] + 1)
                else:
                    term *= (x[int(lit) - 1])
            value += term
        return value
    
    def count_integral_points(n):
        count = 0
        for x in range(-n, n + 1):
            if evaluate_quadratic_form(literals, clauses, [x] * n) == 0:
                count += 1
        return count
    
    def resolution_width(clauses):
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n = random.randint(5, 40)
    literals, clauses = generate_tseitin_formula(n)
    integral_points = count_integral_points(n)
    proof_width = resolution_width(clauses)
    
    return {
        "metric_name": "integral_points",
        "metric_value": integral_points,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": integral_points > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")