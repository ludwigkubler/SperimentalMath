# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_formula(n: int) -> list:
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals + [f'-{lit}' for lit in literals], 2)
        clauses.append(clause)
    return clauses

def dpll_search_tree(formula: list) -> int:
    def solve(lits_true, lits_false):
        if not formula:
            return 1
        literal = random.choice([l for l in lits_true + lits_false if l[0] != '-'])
        new_lits_true = [lit for lit in lits_true if lit != literal and f'-{lit}' not in lits_false]
        new_lits_false = [lit for lit in lits_false if lit != literal and f'-{lit}' not in lits_true]
        return solve(new_lits_true, new_lits_false) + solve(new_lits_false, new_lits_true)
    return solve([f'x{i}' for i in range(1, len(formula)+1)], [f'-x{i}' for i in range(1, len(formula)+1)])

def topological_entropy(n: int) -> float:
    if n == 0:
        return 0
    return math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_random_formula(n)
        h_phi = topological_entropy(len(formula))
        L_phi = dpll_search_tree(formula)
        
        if h_phi == 0 or L_phi == 0:
            continue
        
        results.append((h_phi, L_phi))
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_x = sum(x for x, _ in results) / len(results)
    mean_y = sum(y for _, y in results) / len(results)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in results)
    denominator = math.sqrt(sum((x - mean_x)**2 for x, _ in results) * sum((y - mean_y)**2 for _, y in results))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and all(abs(h_phi - L_phi) <= 10 for h_phi, L_phi in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    total_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        total_results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in total_results):
        mean_value = sum(result["metric_value"] for result in total_results) / len(total_results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in total_results) / len(total_results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, total_results) if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in total_results) / len(total_results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in total_results) / len(total_results))
        support_fraction = sum(1 for result in total_results if result["conjecture_holds"]) / len(total_results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in total_results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")