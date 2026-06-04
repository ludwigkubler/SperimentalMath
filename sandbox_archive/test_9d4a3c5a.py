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
        clauses = []
        for _ in range(random.randint(5, 10)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def geometric_quantization_rank(cnf):
        # Placeholder implementation; actual computation depends on the conjecture
        return len(cnf)
    
    def resolution_proof_width(cnf):
        # Placeholder implementation; actual computation depends on the conjecture
        return len(cnf) * 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        gqrank = geometric_quantization_rank(cnf)
        w = resolution_proof_width(cnf)
        results.append({"n": n, "gqrank": gqrank, "w": w})
    
    if not results:
        return {
            "metric_name": "gqrank_w_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    gqsum = sum(result["gqrank"] for result in results)
    wsum = sum(result["w"] for result in results)
    nsum = sum(result["n"] for result in results)
    n2sum = sum(result["n"] ** 2 for result in results)
    gwprodsum = sum(result["gqrank"] * result["w"] for result in results)
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = True
    counterexample = ""
    
    if instances_tested < 30:
        return {
            "metric_name": "gqrank_w_correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    if n_max < 16:
        return {
            "metric_name": "gqrank_w_correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    n = instances_tested
    gqmean = gqsum / n
    wmean = wsum / n
    nbar = n2sum / n
    
    covariance = gwprodsum - (gqmean * wmean)
    variance_gqrank = sum((result["gqrank"] - gqmean) ** 2 for result in results) / n
    variance_w = sum((result["w"] - wmean) ** 2 for result in results) / n
    
    if variance_gqrank == 0 or variance_w == 0:
        return {
            "metric_name": "gqrank_w_correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_gqrank) * math.sqrt(variance_w))
    
    if abs(correlation_coefficient) < 0.8:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "gqrank_w_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials")
        sys.exit(0)
    
    gqrank_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    instances_tested = sum(result["instances_tested"] for result in results)
    n_max = max(result["n_max"] for result in results)
    
    if len(gqrank_values) < 30:
        print(f"RESULT: INCONCLUSIVE insufficient_instances n_tested={len(gqrank_values)}")
        sys.exit(0)
    
    if n_max < 16:
        print(f"RESULT: INCONCLUSIVE insufficient_n n_max={n_max}")
        sys.exit(0)
    
    mean = sum(gqrank_values) / len(gqrank_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in gqrank_values) / len(gqrank_values))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{0.8}\" first_failing_seed={first_failing_seed}")