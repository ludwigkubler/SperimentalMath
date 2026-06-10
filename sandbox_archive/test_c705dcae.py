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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree_height(clauses):
        stack = [(clauses, [])]
        max_height = 0
        while stack:
            clauses, path = stack.pop()
            if not clauses:
                max_height = max(max_height, len(path))
                continue
            literal = clauses[0][0]
            new_clauses = [c for c in clauses if literal not in c and f'~{literal}' not in c]
            stack.append((new_clauses, path + [(literal, 'T')]))
            stack.append((new_clauses, path + [(f'~{literal}', 'F')]))
        return max_height
    
    def construct_braided_monoidal_category(clauses):
        # Simplified representation using a dictionary to count generators
        generator_count = 0
        for clause in clauses:
            for literal in clause:
                if literal.startswith('~'):
                    continue
                generator_count += 1
        return generator_count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        height = dpll_search_tree_height(formula)
        generators = construct_braided_monoidal_category(formula)
        
        results.append({
            "n": n,
            "height": height,
            "generators": generators
        })
    
    if not results:
        return {
            "metric_name": "DPLL Search Tree Height",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(r["n"] for r in results)
    if n_max < 16:
        return {
            "metric_name": "DPLL Search Tree Height",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    heights = [r["height"] for r in results]
    generators = [r["generators"] for r in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    correlation = pearson_correlation(heights, generators)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation > 0.8,
        "counterexample": "" if correlation >= 0.5 else f"correlation={correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_below_0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")