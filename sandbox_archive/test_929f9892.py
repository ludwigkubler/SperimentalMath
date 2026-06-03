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
            return "x"
        else:
            p = random.choice(["AND", "OR"])
            a, b = generate_formula(n // 2), generate_formula(n - n // 2)
            return f"({a} {p} {b})"
    
    def dpll(formula):
        if formula == "true":
            return 0
        elif formula == "false":
            return float('inf')
        elif formula[0] in "xX":
            return 1
        else:
            p, a, b = formula.split()
            return 1 + min(dpll(a), dpll(b))
    
    def regular_grammar_order(formula):
        if formula == "true" or formula == "false":
            return 0
        elif formula[0] in "xX":
            return 1
        else:
            p, a, b = formula.split()
            return 1 + max(regular_grammar_order(a), regular_grammar_order(b))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        dpll_length = dpll(formula)
        grammar_order = regular_grammar_order(formula)
        results.append({"n": n, "dpll_length": dpll_length, "grammar_order": grammar_order})
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    dpll_lengths = [r["dpll_length"] for r in results]
    grammar_orders = [r["grammar_order"] for r in results]
    
    mean_dpll = sum(dpll_lengths) / len(dpll_lengths)
    mean_grammar = sum(grammar_orders) / len(grammar_orders)
    
    cov = sum((d - mean_dpll) * (g - mean_grammar) for d, g in zip(dpll_lengths, grammar_orders))
    var_dpll = sum((d - mean_dpll) ** 2 for d in dpll_lengths)
    var_grammar = sum((g - mean_grammar) ** 2 for g in grammar_orders)
    
    if var_dpll == 0 or var_grammar == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    pearson_corr = cov / math.sqrt(var_dpll * var_grammar)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: INCONCLUSIVE reason=unknown")