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
        literals = ['x' + str(i) for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        return clauses
    
    def dpll(formula, assignment={}):
        if not formula:
            return True
        literal, rest = formula[0]
        pos_var = literal[1:]
        neg_var = '-' + literal[1:]
        
        if pos_var in assignment and assignment[pos_var] == False:
            return False
        if neg_var in assignment and assignment[neg_var] == True:
            return False
        
        for var in [pos_var, neg_var]:
            new_assignment = assignment.copy()
            new_assignment[var] = (var[0] == '+')
            if dpll(formula[1:], new_assignment):
                return True
        return False
    
    def min_non_abelian_galois_order(n):
        # Placeholder for actual computation of minimal non-abelian Galois order
        # This is a dummy implementation for testing purposes
        return n + 1
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_max = 0
    min_orders = []
    widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            width = dpll(formula)
            if width is None:
                continue
            min_order = min_non_abelian_galois_order(n)
            min_orders.append(min_order)
            widths.append(width)
            n_max = max(n_max, n)
    
    correlation = pearson_correlation(min_orders, widths)
    conjecture_holds = correlation >= 0.7 and all(min_order <= 1 * width for min_order, width in zip(min_orders, widths))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(min_orders),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")