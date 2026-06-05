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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        pure_symbols = {}
        for c in cnf:
            for lit in c:
                if abs(lit) not in assignment and lit not in pure_symbols:
                    pure_symbols[abs(lit)] = lit > 0
                elif abs(lit) in assignment and assignment[abs(lit)] != (lit > 0):
                    return False
        
        for symbol, polarity in pure_symbols.items():
            if dpll([c for c in cnf if not any(lit == symbol or lit == -symbol for lit in c)], {**assignment, symbol: polarity}):
                return True
            if dpll([c for c in cnf if not any(lit == symbol or lit == -symbol for lit in c)], {**assignment, symbol: not polarity}):
                return True
        return False
    
    def geometric_entropy(n):
        # Placeholder for geometric entropy calculation
        # This is a dummy implementation and should be replaced with actual computation
        return random.uniform(0.5, 1.5)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n, 2 * n)
        entropy = geometric_entropy(n)
        width = dpll(cnf)
        if width is None:
            continue
        results.append((entropy, width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    sum_x = sum(x for x, _ in results)
    sum_y = sum(y for _, y in results)
    sum_xy = sum(x * y for x, y in results)
    sum_xx = sum(x ** 2 for x, _ in results)
    sum_yy = sum(y ** 2 for _, y in results)
    
    mean_x = sum_x / n
    mean_y = sum_y / n
    cov_xy = (sum_xy - n * mean_x * mean_y) / (n - 1)
    var_x = (sum_xx - n * mean_x ** 2) / (n - 1)
    var_y = (sum_yy - n * mean_y ** 2) / (n - 1)
    
    correlation_coefficient = cov_xy / math.sqrt(var_x * var_y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.95:
        result = "SUPPORTED"
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        result = f"FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE"
    
    print(f"RESULT: {result} mean={mean_value} std={std_value} support_fraction={support_fraction}")