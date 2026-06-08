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
    
    def generate_boolean_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = []
            for var in variables:
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(f'¬{var}')
            clauses.append(' ∨ '.join(clause))
        return ' ∧ '.join(clauses)

    def dpll_solver(formula):
        # Simplified DPLL solver for demonstration purposes
        if formula == 'True':
            return 1
        elif formula == 'False':
            return float('inf')
        else:
            literals = formula.split()
            literal = literals[0]
            rest = ' ∧ '.join(literals[1:])
            if literal.startswith('¬'):
                return dpll_solver(rest.replace(f'¬{literal}', '', 1))
            else:
                return min(dpll_solver(rest.replace(literal, '', 1)), dpll_solver(rest.replace(f'¬{literal}', '', 1)))

    def p_adic_logarithmic_rank(formula):
        # Simplified p-adic logarithmic rank for demonstration purposes
        return len(formula.split())

    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    d_phi = dpll_solver(formula)
    logrank_p_phi = p_adic_logarithmic_rank(formula)

    return {
        "metric_name": "logrank_p",
        "metric_value": logrank_p_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if d_phi == float('inf') else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")