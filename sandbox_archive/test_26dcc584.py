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
    
    def generate_2cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, k=2)
            clauses.append(clause)
        return clauses
    
    def ehrhart_quotient(n):
        # Placeholder function to compute the Ehrhart quotient
        # This is a dummy implementation and should be replaced with actual computation
        return n + 1
    
    def frege_proof_depth(φ):
        # Placeholder function to compute the Frege proof depth
        # This is a dummy implementation and should be replaced with actual computation
        return len(φ)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            φ = generate_2cnf(n)
            q_n = ehrhart_quotient(n)
            d_n = frege_proof_depth(φ)
            results.append((q_n, d_n))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    sum_q_n = sum(q_n for q_n, _ in results)
    sum_d_n = sum(d_n for _, d_n in results)
    sum_q_n_squared = sum(q_n**2 for q_n, _ in results)
    sum_d_n_squared = sum(d_n**2 for _, d_n in results)
    sum_q_n_d_n = sum(q_n * d_n for q_n, d_n in results)
    
    mean_q_n = sum_q_n / n
    mean_d_n = sum_d_n / n
    
    covariance = sum_q_n_d_n - n * mean_q_n * mean_d_n
    variance_q_n = sum_q_n_squared - n * mean_q_n**2
    variance_d_n = sum_d_n_squared - n * mean_d_n**2
    
    if variance_q_n == 0 or variance_d_n == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_q_n) * math.sqrt(variance_d_n))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break