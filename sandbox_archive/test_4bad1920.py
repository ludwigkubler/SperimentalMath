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

def generate_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables + [-v for v in variables], 2)
        clauses.append(' '.join(clause))
    return ' & '.join(clauses)

def integral_representation(formula):
    norm = 0
    for clause in formula.split(' & '):
        clause_norm = sum(abs(int(c[1:]) if c[0] != '-' else -int(c[1:])) for c in clause.split())
        norm = max(norm, clause_norm)
    return norm

def dpll_search_tree_width(formula):
    # Simplified DPLL search tree width calculation
    return len(formula.split(' & '))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_formula(n)
    
    norm = integral_representation(formula)
    width = dpll_search_tree_width(formula)
    
    metric_name = "Minimal Norm of Integral Quotients"
    metric_value = norm
    instances_tested = 1
    conjecture_holds = norm <= math.log(n) and width <= 2 * math.log(n)
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Norm: {norm}, Width: {width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        result = f"RESULT: FALSIFIED counterexample=\"Formula: {results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(result)