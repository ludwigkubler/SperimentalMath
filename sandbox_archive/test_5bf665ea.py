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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|'])
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def dpll(formula):
        if formula == 'True':
            return 1
        elif formula == 'False':
            return float('inf')
        else:
            var, op, subformula = formula.split()
            if op == '&':
                return min(dpll(subformula), dpll(f'({var} -> {subformula})'))
            elif op == '|':
                return max(dpll(subformula), dpll(f'(¬{var} -> {subformula})'))
    
    def p_adic_order(n):
        if n == 0:
            return float('inf')
        count = 0
        while n % 2 == 0:
            n //= 2
            count += 1
        return count
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        path_length = dpll(formula)
        p_order = p_adic_order(path_length)
        results.append((n, p_order, path_length))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    p_orders = [p_order for _, p_order, _ in results]
    path_lengths = [path_length for _, _, path_length in results]
    mean_p_order = sum(p_orders) / len(p_orders)
    mean_path_length = sum(path_lengths) / len(path_lengths)
    correlation = sum((p_order - mean_p_order) * (path_length - mean_path_length) for p_order, path_length in zip(p_orders, path_lengths)) / (len(results) * math.sqrt(sum((p_order - mean_p_order)**2 for p_order in p_orders) * sum((path_length - mean_path_length)**2 for path_length in path_lengths)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")