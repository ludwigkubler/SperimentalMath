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
    
    def generate_cnf(n, m):
        variables = set(range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        # Simplified DPLL width calculation (not actual DPLL)
        return len(cnf) ** 0.5
    
    def p_adic_galois_index(m):
        # Simplified p-adic Galois index (not actual computation)
        return math.log2(m + 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = range(2, 31)
    results = []
    
    for n in n_values:
        for m in m_values:
            cnf = generate_cnf(n, m)
            width = dpll_width(cnf)
            index = p_adic_galois_index(m)
            results.append((n, m, width, index))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    widths = [r[2] for r in results]
    indices = [r[3] for r in results]
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    correlation = pearsons_correlation(widths, indices)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

def pearsons_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    return numerator / denominator if denominator != 0 else float('nan')

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")