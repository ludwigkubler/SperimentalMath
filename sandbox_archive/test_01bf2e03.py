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
    
    def generate_sat_instance(n):
        literals = set(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        return clauses

    def tseitin_formula(clauses):
        variables = {}
        counter = 0
        for clause in clauses:
            counter += 1
            var_name = f'p{counter}'
            variables[var_name] = clause
        return variables

    def resolution_proof_width(variables):
        width = max(len(clause) for clause in variables.values())
        return width

    def groupoid_cospans(variables):
        cospans = {}
        for var, clause in variables.items():
            if len(clause) == 2:
                a, b = clause
                if (a, b) not in cospans:
                    cospans[(a, b)] = []
                if (b, a) not in cospans:
                    cospans[(b, a)] = []
        return cospans

    def min_index(cospans):
        indices = {}
        for (a, b), cospan in cospans.items():
            if len(cospan) == 0:
                continue
            index = sum(len(clause) for clause in cospan)
            indices[(a, b)] = index
        return max(indices.values())

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sat_instance = generate_sat_instance(n)
        tseitin_vars = tseitin_formula(sat_instance)
        proof_width = resolution_proof_width(tseitin_vars)
        cospans = groupoid_cospans(tseitin_vars)
        index = min_index(cospans)
        
        results.append({
            "n": n,
            "proof_width": proof_width,
            "index": index
        })

    metric_values = [result["index"] for result in results]
    widths = [result["proof_width"] for result in results]

    if len(metric_values) < 30:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_index = sum(metric_values) / len(metric_values)
    std_dev_index = math.sqrt(sum((x - mean_index) ** 2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = sum((metric_values[i] - mean_index) * (widths[i] - mean_width) for i in range(len(results))) / (len(results) * std_dev_index * mean_width)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.6 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")