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
    
    def generate_random_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            left = generate_random_boolean_formula(n // 2)
            right = generate_random_boolean_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def dpll(formula):
        if formula == 'True':
            return 1
        elif formula == 'False':
            return float('inf')
        else:
            var, op, subformula = formula[1:-1].split()
            if op == 'and':
                return min(dpll(subformula) for subformula in subformula.split(op))
            elif op == 'or':
                return max(dpll(subformula) for subformula in subformula.split(op))
    
    def regular_grammar_order(formula):
        if formula == 'True' or formula == 'False':
            return 1
        else:
            var, op, subformula = formula[1:-1].split()
            if op == 'and':
                return sum(regular_grammar_order(subformula) for subformula in subformula.split(op))
            elif op == 'or':
                return max(regular_grammar_order(subformula) for subformula in subformula.split(op)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_random_boolean_formula(n)
        dpll_length = dpll(formula)
        grammar_order = regular_grammar_order(formula)
        
        if dpll_length == float('inf'):
            continue
        
        results.append({
            "n": n,
            "dpll_length": dpll_length,
            "grammar_order": grammar_order
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    dpll_lengths = [r["dpll_length"] for r in results]
    grammar_orders = [r["grammar_order"] for r in results]
    
    mean_dpll_length = sum(dpll_lengths) / len(dpll_lengths)
    mean_grammar_order = sum(grammar_orders) / len(grammar_orders)
    
    covariance = sum((d - mean_dpll_length) * (g - mean_grammar_order) for d, g in zip(dpll_lengths, grammar_orders))
    variance_dpll = sum((d - mean_dpll_length) ** 2 for d in dpll_lengths)
    variance_grammar = sum((g - mean_grammar_order) ** 2 for g in grammar_orders)
    
    if variance_dpll == 0 or variance_grammar == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_dpll) * math.sqrt(variance_grammar))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")