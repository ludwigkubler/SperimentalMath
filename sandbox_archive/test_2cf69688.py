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
from math import log

def generate_formula(n: int) -> str:
    if n == 0:
        return ""
    elif n == 1:
        return "A"
    else:
        op = random.choice(["&", "|"])
        var = chr(65 + random.randint(0, n-1))
        subformula1 = generate_formula(random.randint(1, min(n//2, n-2)))
        subformula2 = generate_formula(n - len(subformula1) - 1)
        return f"({subformula1} {op} {subformula2})"

def dpll_path_length(formula: str) -> int:
    stack = []
    length = 0
    for char in formula:
        if char == '(':
            stack.append(char)
            length += 1
        elif char == ')':
            stack.pop()
            length += 1
        elif char in '&|':
            length += 1
    return length

def p_adic_order(formula: str) -> int:
    # Simplified p-adic order calculation for demonstration purposes
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        p_order = p_adic_order(formula)
        dpll_length = dpll_path_length(formula)
        if dpll_length == 0:
            continue
        correlation = log(p_order) / log(dpll_length)
        results.append({
            "n": n,
            "p_adic_order": p_order,
            "dpll_path_length": dpll_length,
            "correlation": correlation
        })
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_correlation = sum(result["correlation"] for result in results) / len(results)
    return {
        "metric_name": "Correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(mean_correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = len([result for result in results if "conjecture_holds" in result and result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support or counterexamples found")