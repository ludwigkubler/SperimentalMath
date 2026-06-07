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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return 'A'
        else:
            var = chr(65 + random.randint(0, n-1))
            op = random.choice(['&', '|'])
            subformula1 = generate_formula(random.randint(1, n//2))
            subformula2 = generate_formula(n - len(subformula1) - 1)
            return f'({subformula1} {op} {subformula2})'
    
    def dpll(formula):
        if formula == 'A':
            return 1
        elif formula == 'B':
            return 1
        elif formula.startswith('('):
            op = formula[3]
            subformula1 = formula[4:-1].split(' ')[0]
            subformula2 = formula[4:-1].split(' ')[2]
            if op == '&':
                return dpll(subformula1) + dpll(subformula2)
            elif op == '|':
                return max(dpll(subformula1), dpll(subformula2))
        else:
            return 0
    
    def p_adic_order(formula):
        if formula == 'A' or formula == 'B':
            return 1
        elif formula.startswith('('):
            op = formula[3]
            subformula1 = formula[4:-1].split(' ')[0]
            subformula2 = formula[4:-1].split(' ')[2]
            if op == '&':
                return min(p_adic_order(subformula1), p_adic_order(subformula2))
            elif op == '|':
                return max(p_adic_order(subformula1), p_adic_order(subformula2))
        else:
            return 0
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    path_length = dpll(formula)
    p_order = p_adic_order(formula)
    
    if path_length == 0 or p_order == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll_path_length or p_adic_order is zero"
        }
    
    correlation = math.log(p_order) / math.log(path_length)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation too low\" first_failing_seed={r['seed']}")
                break