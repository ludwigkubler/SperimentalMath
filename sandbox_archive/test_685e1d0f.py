# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        # Simplified DPLL algorithm to estimate width
        variables = set()
        for clause in cnf:
            variables.update(abs(x) for x in clause)
        
        def solve(model, literals):
            if not literals:
                return True
            literal = literals[0]
            pos_var = abs(literal)
            neg_var = -pos_var
            
            if pos_var not in model and neg_var not in model:
                if solve(model | {pos_var: True}, literals[1:]):
                    return True
                elif solve(model | {neg_var: False}, literals[1:]):
                    return True
            elif pos_var in model and model[pos_var]:
                if solve(model, literals[1:]):
                    return True
            elif neg_var in model and not model[neg_var]:
                if solve(model, literals[1:]):
                    return True
            return False
        
        max_width = 0
        for literal_set in combinations(variables, len(variables)):
            model = {}
            if solve(model, list(literal_set)):
                width = len([x for x in literal_set if x in model and model[x]])
                max_width = max(max_width, width)
        return max_width
    
    def min_representation_length(cnf):
        # Simplified algebraic statistics minimal representation length
        variables = set()
        for clause in cnf:
            variables.update(abs(x) for x in clause)
        return len(variables) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            width = dpll_width(cnf)
            length = min_representation_length(cnf)
            results.append((n, width, length))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, widths, lengths = zip(*results)
    mean_width = sum(widths) / len(widths)
    mean_length = sum(lengths) / len(lengths)
    corr_coeff = sum((w - mean_width) * (l - mean_length) for w, l in zip(widths, lengths)) / (len(widths) * math.sqrt(sum((w - mean_width) ** 2 for w in widths) * sum((l - mean_length) ** 2 for l in lengths)))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= corr_coeff < 0.7,
        "counterexample": "" if 0.5 <= corr_coeff < 0.7 else f"Correlation coefficient {corr_coeff} is outside the acceptable range [0.5, 0.7)"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(2, 6)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if 0.5 <= result["metric_value"] < 0.7) / len(results)
    
    if all(0.5 <= result["metric_value"] < 0.7 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=NA support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")