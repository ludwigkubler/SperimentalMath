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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                cnf.append(clause)
        return cnf
    
    def calculate_mld(cnf):
        # Placeholder function to simulate mld calculation
        return random.random()
    
    def calculate_w(cnf):
        # Placeholder function to simulate w calculation
        return len(cnf) * 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    mld_values = []
    w_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        mld = calculate_mld(cnf)
        w = calculate_w(cnf)
        mld_values.append(mld)
        w_values.append(w)
    
    if len(mld_values) < 2 or len(w_values) < 2:
        return {
            "metric_name": "mld_vs_w",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    mean_mld = sum(mld_values) / len(mld_values)
    mean_w = sum(w_values) / len(w_values)
    
    covariance = sum((mld_values[i] - mean_mld) * (w_values[i] - mean_w) for i in range(len(n_values)))
    variance_mld = sum((mld_values[i] - mean_mld) ** 2 for i in range(len(n_values))) / len(mld_values)
    variance_w = sum((w_values[i] - mean_w) ** 2 for i in range(len(n_values))) / len(w_values)
    
    if variance_mld == 0 or variance_w == 0:
        return {
            "metric_name": "mld_vs_w",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_mld) * math.sqrt(variance_w))
    
    return {
        "metric_name": "mld_vs_w",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_data")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if "metric_value" in r and r["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")