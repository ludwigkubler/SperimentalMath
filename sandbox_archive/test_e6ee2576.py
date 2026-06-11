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

def generate_instance(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def dpll_width(instance):
    n = len(instance)
    if n == 0:
        return 0
    if all(x == 0 or x == 1 for x in instance):
        return 1
    
    # Find a literal to branch on
    literals = [i for i, x in enumerate(instance) if x != 2]
    if not literals:
        return 1
    
    lit = random.choice(literals)
    
    positive_clauses = []
    negative_clauses = []
    for clause in instance:
        if clause[lit] == 0:
            negative_clauses.append(clause[:lit] + [2] + clause[lit+1:])
        elif clause[lit] == 1:
            positive_clauses.append(clause[:lit] + [2] + clause[lit+1:])
    
    return max(dpll_width(positive_clauses), dpll_width(negative_clauses))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mld_values = []
    w_dpll_values = []
    
    for n in n_values:
        instances = [generate_instance(n) for _ in range(30)]
        mld_values.extend([sum(x != 2 for x in instance) for instance in instances])
        w_dpll_values.extend([dpll_width(instance) for instance in instances])
    
    if not mld_values or not w_dpll_values:
        return {
            "metric_name": "mld_w_dpll_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }
    
    mld_mean = sum(mld_values) / len(mld_values)
    w_dpll_mean = sum(w_dpll_values) / len(w_dpll_values)
    correlation_coefficient = sum((m - mld_mean) * (w - w_dpll_mean) for m, w in zip(mld_values, w_dpll_values)) / math.sqrt(sum((m - mld_mean)**2 for m in mld_values) * sum((w - w_dpll_mean)**2 for w in w_dpll_values))
    
    return {
        "metric_name": "mld_w_dpll_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mld_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(m - w) <= 3 for m, w in zip(mld_values, w_dpll_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean = None
        std_dev = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean} std={std_dev} support_fraction={support_fraction}")