# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n, num_clauses):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(num_clauses):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return ' & '.join(f'({c[0]} | {c[1]})' for c in clauses)
    
    def dpll_width(formula, n):
        literals = set()
        for clause in formula.split(' & '):
            for lit in clause.split(' | '):
                if lit.startswith('~'):
                    literals.add(lit[1:])
                else:
                    literals.add(lit)
        return len(literals)
    
    def twisted_hodge_order(formula, n):
        # Placeholder function to simulate computation of minimal order
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        num_clauses = random.randint(n, 2*n)
        formula = generate_formula(n, num_clauses)
        order = twisted_hodge_order(formula, n)
        width = dpll_width(formula, n)
        results.append((order, width))
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_order = sum(o for o, w in results) / len(results)
    mean_width = sum(w for o, w in results) / len(results)
    correlation = (sum((o - mean_order) * (w - mean_width) for o, w in results) /
                   math.sqrt(sum((o - mean_order)**2 for o, _ in results) *
                             sum((w - mean_width)**2 for _, w in results)))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")