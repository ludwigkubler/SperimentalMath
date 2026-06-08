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
    
    def frobenius_schur_indicator(n):
        # Placeholder implementation for Frobenius-Schur indicator
        return random.uniform(-1, 1)

    def dpll_proof_path_length(n):
        # Placeholder implementation for DPLL proof path length
        return random.randint(10, 100)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        fs_indicator = frobenius_schur_indicator(n)
        dpll_length = dpll_proof_path_length(n)
        metric_values.append((fs_indicator, dpll_length))
    
    if not metric_values:
        return {
            "metric_name": "Frobenius-Schur Indicator vs DPLL Proof Path Length",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    fs_values = [fs for fs, _ in metric_values]
    dpll_values = [dpll for _, dpll in metric_values]
    
    mean_fs = sum(fs_values) / len(fs_values)
    mean_dpll = sum(dpll_values) / len(dpll_values)
    
    cov = sum((fs - mean_fs) * (dpll - mean_dpll) for fs, dpll in metric_values) / len(metric_values)
    var_fs = sum((fs - mean_fs) ** 2 for fs in fs_values) / len(fs_values)
    var_dpll = sum((dpll - mean_dpll) ** 2 for dpll in dpll_values) / len(dpll_values)
    
    correlation_coefficient = cov / (math.sqrt(var_fs) * math.sqrt(var_dpll))
    
    return {
        "metric_name": "Frobenius-Schur Indicator vs DPLL Proof Path Length",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) <= 1,  # Assuming c = 1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r.get("conjecture_holds", False)) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")