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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, n-1) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def compute_local_cohomology(cnf):
        # Simplified local cohomology computation (not actual implementation)
        return len(cnf)
    
    def measure_frege_proof_length(cnf):
        # Placeholder for SAT solver
        return random.randint(10, 100)
    
    n = 5
    lcoh_values = []
    f_values = []
    
    for _ in range(30):
        cnf = generate_cnf(n)
        lcoh = compute_local_cohomology(cnf)
        f = measure_frege_proof_length(cnf)
        lcoh_values.append(lcoh)
        f_values.append(f)
    
    if not lcoh_values or not f_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(lcoh_values),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_lists"
        }
    
    correlation_coefficient = sum((x - mean_lcoh) * (y - mean_f) for x, y in zip(lcoh_values, f_values)) / \
                               math.sqrt(sum((x - mean_lcoh)**2 for x in lcoh_values) * sum((y - mean_f)**2 for y in f_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(lcoh_values),
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 or not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")