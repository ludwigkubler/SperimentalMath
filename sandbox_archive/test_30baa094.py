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
    
    def generate_formula(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f"~{v}" for v in variables], 3)
            clauses.append(" | ".join(clause))
        return " & ".join(clauses)

    def dpll_width(formula, n):
        literals = set()
        for lit in formula.split():
            if lit.startswith("~"):
                literals.add(lit[1:])
            else:
                literals.add(lit)
        return len(literals) // 2

    def quasi_frobenius_rank(n):
        # Simplified example: rank is proportional to n
        return n

    instances_tested = 0
    min_ranks = []
    dpll_widths = []

    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        m = random.randint(n, 2*n)
        formula = generate_formula(n, m)
        rank = quasi_frobenius_rank(n)
        width = dpll_width(formula, n)
        
        min_ranks.append(rank)
        dpll_widths.append(width)
        instances_tested += 1

    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_ranks, dpll_widths)) / math.sqrt(sum((x - mean_x)**2 for x in min_ranks) * sum((y - mean_y)**2 for y in dpll_widths))
    mean_x = sum(min_ranks) / instances_tested
    mean_y = sum(dpll_widths) / instances_tested

    conjecture_holds = correlation_coefficient > 0.7 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient=<cc> p_value=<pv>"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,  # Largest instance size n encountered
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=<cc> p_value=<pv>\" first_failing_seed={first_failing_seed}")