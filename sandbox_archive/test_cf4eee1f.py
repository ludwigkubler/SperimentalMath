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
    
    def generate_instance(n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(literals) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def mld(instance):
        if not instance:
            return 0
        literals = set()
        for clause in instance:
            literals.update(clause)
        return len(literals)
    
    def dpll_width(instance):
        if not instance:
            return 0
        max_width = 0
        for literal in range(-len(instance), len(instance) + 1):
            positive_clauses = [clause for clause in instance if literal in clause]
            negative_clauses = [clause for clause in instance if -literal in clause]
            width = max(dpll_width(positive_clauses), dpll_width(negative_clauses))
            max_width = max(max_width, width + 1)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    mld_values = []
    w_dpll_values = []
    
    for n in n_values:
        instances = [generate_instance(n) for _ in range(5)]
        mld_values.extend([mld(instance) for instance in instances])
        w_dpll_values.extend([dpll_width(instance) for instance in instances])
    
    if len(mld_values) < 30 or len(w_dpll_values) < 30:
        return {
            "metric_name": "mld_vs_w_dpll",
            "metric_value": None,
            "instances_tested": len(mld_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_mld = sum(mld_values) / len(mld_values)
    mean_w_dpll = sum(w_dpll_values) / len(w_dpll_values)
    correlation_coefficient = sum((mld - mean_mld) * (w_dpll - mean_w_dpll) for mld, w_dpll in zip(mld_values, w_dpll_values)) / (len(mld_values) * math.sqrt(sum((mld - mean_mld)**2 for mld in mld_values)) * math.sqrt(sum((w_dpll - mean_w_dpll)**2 for w_dpll in w_dpll_values)))
    
    return {
        "metric_name": "mld_vs_w_dpll",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mld_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(mld - w_dpll) <= 3 for mld, w_dpll in zip(mld_values, w_dpll_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_linearly_correlated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")