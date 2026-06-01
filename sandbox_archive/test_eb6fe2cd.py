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
    
    def generate_2cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        # Simplified Frege proof depth estimation
        return len(cnf) * 2
    
    def ehrhart_quotient(n):
        # Simplified Ehrhart quotient estimation
        return n ** 2 / (n + 1)
    
    results = []
    for _ in range(30):  # Test with 30 instances per seed
        n = random.randint(5, 40)  # Sweep through sizes 5 to 40
        cnf = generate_2cnf(n)
        depth = frege_proof_depth(cnf)
        quotient = ehrhart_quotient(n)
        results.append({"n": n, "depth": depth, "quotient": quotient})
    
    if not results:
        return {
            "metric_name": "Ehrhart Quotient vs. Frege Proof Depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_values = [r["n"] for r in results]
    depth_values = [r["depth"] for r in results]
    quotient_values = [r["quotient"] for r in results]
    
    mean_depth = sum(depth_values) / len(depth_values)
    mean_quotient = sum(quotient_values) / len(quotient_values)
    
    covariance = sum((d - mean_depth) * (q - mean_quotient) for d, q in zip(depth_values, quotient_values))
    variance_depth = sum((d - mean_depth) ** 2 for d in depth_values)
    variance_quotient = sum((q - mean_quotient) ** 2 for q in quotient_values)
    
    if variance_depth == 0 or variance_quotient == 0:
        return {
            "metric_name": "Ehrhart Quotient vs. Frege Proof Depth",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Zero variance in depth or quotient"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_quotient))
    
    return {
        "metric_name": "Ehrhart Quotient vs. Frege Proof Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results) if any(r["metric_value"] is not None for r in results) else None
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results)) if any(r["metric_value"] is not None for r in results) else None
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if all(r["metric_value"] is not None for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")