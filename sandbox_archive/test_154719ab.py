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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(n-1):
            clauses.append([f'~{variables[i]}', f'{variables[i+1]}'])
        return clauses, variables
    
    def generate_coxeter_group(clauses, variables):
        n = len(variables)
        group = set()
        for clause in clauses:
            for var in clause:
                if var.startswith('~'):
                    group.add((var[1:], False))
                else:
                    group.add((var, True))
        return group
    
    def min_reflections(group):
        reflections = 0
        for element in group:
            if not element[1]:
                reflections += 1
        return reflections
    
    def resolution_width(clauses):
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            clauses, variables = tseitin_formula(n)
            group = generate_coxeter_group(clauses, variables)
            r = min_reflections(group)
            w = resolution_width(clauses)
            results.append((n, r, w))
    
    if not results:
        return {
            "metric_name": "resolution_width_over_r_squared",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(n for _, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "resolution_width_over_r_squared",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    metric_values = [w / (r ** 2) for _, r, w in results]
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "resolution_width_over_r_squared",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": all(0.9 <= x / (r ** 2) <= 1.1 for _, r, w in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value:.6f} std={std_value:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction:.2f}")