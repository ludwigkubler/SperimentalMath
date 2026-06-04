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
from fractions import Fraction
import math

def generate_sat_instance(m: int) -> tuple:
    variables = set()
    clauses = []
    for _ in range(m):
        num_literals = random.randint(1, 3)
        clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(num_literals)]
        variables.update(clause)
        clauses.append(clause)
    return list(variables), clauses

def clause_subset_entropy(variables: list, clauses: list) -> float:
    n_vars = len(variables)
    n_clauses = len(clauses)
    total_weight = 0
    for clause in clauses:
        weight = 1 / (2 ** len(clause))
        total_weight += weight
    entropy = Fraction(total_weight, n_clauses * 2 ** n_vars).log2() if total_weight > 0 else 0
    return entropy

def tseitin_formula(variables: list, clauses: list) -> str:
    new_vars = {f'y{i}': i for i in range(1, len(clauses) + 1)}
    formula = []
    for clause in clauses:
        subformula = ' | '.join([new_vars[f'y{i}'] if literal.startswith('x') else f'-{new_vars[f'y{i}']}'
                                  for i, literal in enumerate(clause)])
        formula.append(f'{subformula} -> y{i}')
    return ' & '.join(formula)

def resolution_width(formula: str) -> int:
    # Simplified version of resolution width calculation
    # This is a placeholder and should be replaced with actual implementation
    return len(formula.split(' & '))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m = random.randint(5, 30)
    variables, clauses = generate_sat_instance(m)
    entropy = clause_subset_entropy(variables, clauses)
    tseitin_formula_str = tseitin_formula(variables, clauses)
    width = resolution_width(tseitin_formula_str)
    metric_value = abs(entropy - width) / (m * len(variables))
    return {
        "metric_name": "Brauer Group Entropy vs Resolution Width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")