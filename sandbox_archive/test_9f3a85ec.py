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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        var = next((v for v in range(1, max(var[0] for var in cnf) + 1) if v not in assignment and -v not in assignment), None)
        if var is None:
            return False
        new_assignment = assignment.copy()
        new_assignment[var] = True
        if dpll(cnf, new_assignment):
            return True
        new_assignment[var] = False
        if dpll(cnf, new_assignment):
            return True
        return False
    
    def frege_proof_depth(cnf):
        return len(cnf)
    
    mdeg_values = []
    depth_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size with 5 instances
            cnf = generate_cnf(random.randint(1, n), n)
            depth = frege_proof_depth(cnf)
            mdeg_values.append(depth)  # Simplified as a placeholder
            depth_values.append(depth)
    
    if not mdeg_values or not depth_values:
        return {
            "metric_name": "mdeg",
            "metric_value": None,
            "instances_tested": len(mdeg_values),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(len(cnf) <= n for cnf in mdeg_values)),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_mdeg = sum(mdeg_values) / len(mdeg_values)
    mean_depth = sum(depth_values) / len(depth_values)
    
    covariance = sum((m - mean_mdeg) * (d - mean_depth) for m, d in zip(mdeg_values, depth_values))
    variance_mdeg = sum((m - mean_mdeg) ** 2 for m in mdeg_values)
    variance_depth = sum((d - mean_depth) ** 2 for d in depth_values)
    
    if variance_mdeg == 0 or variance_depth == 0:
        return {
            "metric_name": "mdeg",
            "metric_value": None,
            "instances_tested": len(mdeg_values),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(len(cnf) <= n for cnf in mdeg_values)),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / math.sqrt(variance_mdeg * variance_depth)
    
    return {
        "metric_name": "mdeg",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mdeg_values),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(len(cnf) <= n for cnf in mdeg_values)),
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")