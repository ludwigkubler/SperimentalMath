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
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def sat_complexity(cnf):
        # Placeholder function to simulate circuit satisfiability complexity
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)
    
    def mcr(cnf):
        # Placeholder function to simulate minimal tropical cyclotomic polynomial rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        mcr_value = mcr(cnf)
        sat_complexity_value = sat_complexity(cnf)
        results.append((mcr_value, sat_complexity_value))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mcr_values = [r[0] for r in results]
    sat_complexity_values = [r[1] for r in results]
    mean_mcr = sum(mcr_values) / len(mcr_values)
    mean_sat_complexity = sum(sat_complexity_values) / len(sat_complexity_values)
    
    correlation_coefficient = 0
    if len(mcr_values) > 1:
        numerator = sum((mcr_values[i] - mean_mcr) * (sat_complexity_values[i] - mean_sat_complexity) for i in range(len(mcr_values)))
        denominator = math.sqrt(sum((mcr_values[i] - mean_mcr)**2 for i in range(len(mcr_values))) * sum((sat_complexity_values[i] - mean_sat_complexity)**2 for i in range(len(sat_complexity_values))))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")