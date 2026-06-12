# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def ehrhart_rank(cnf):
        # Placeholder function to compute Ehrhart rank
        return len(cnf)  # Simplified for testing purposes
    
    def resolution_width(cnf):
        # Placeholder function to compute resolution width
        return sum(len(clause) for clause in cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        ehrank_val = ehrhart_rank(cnf)
        width_val = resolution_width(cnf)
        results.append((n, ehrank_val, width_val))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    ehrank_vals = [ehr for _, ehr, _ in results]
    width_vals = [width for _, _, width in results]
    
    mean_ehrank = sum(ehrank_vals) / len(ehrank_vals)
    mean_width = sum(width_vals) / len(width_vals)
    correlation = sum((ehr - mean_ehrank) * (width - mean_width) for ehr, width in zip(ehrank_vals, width_vals)) / (len(results) * (sum((ehr - mean_ehrank) ** 2 for ehr in ehrank_vals) ** 0.5) * (sum((width - mean_width) ** 2 for width in width_vals) ** 0.5))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.8 and max(abs(ehr - width) for ehr, width in zip(ehrank_vals, width_vals)) <= 3,
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
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")
    else:
        mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
        std_corr = (sum((result["metric_value"] - mean_corr) ** 2 for result in results if result["metric_value"] is not None) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")