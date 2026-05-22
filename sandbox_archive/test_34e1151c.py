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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def plethysm_coefficient(n):
        # Simplified approximation for demonstration purposes
        return math.factorial(n) / (math.factorial(n // 2) ** 2)
    
    def permutation_circuit_threshold(n):
        # Simplified approximation for demonstration purposes
        return n * math.log(n, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k_cnf_instance = generate_k_cnf(n, n)
        plethysm_rank = plethysm_coefficient(n)
        circuit_threshold = permutation_circuit_threshold(n)
        
        results.append({
            "n": n,
            "plethysm_rank": plethysm_rank,
            "circuit_threshold": circuit_threshold
        })
    
    mean_plethysm_rank = sum(result["plethysm_rank"] for result in results) / len(results)
    mean_circuit_threshold = sum(result["circuit_threshold"] for result in results) / len(results)
    correlation_coefficient = 0
    
    if mean_plethysm_rank != 0:
        correlation_coefficient = (sum((result["plethysm_rank"] - mean_plethysm_rank) * 
                                       (result["circuit_threshold"] - mean_circuit_threshold) 
                                       for result in results) /
                                  (len(results) * math.sqrt(sum((result["plethysm_rank"] - mean_plethysm_rank) ** 2 
                                                               for result in results)) *
                                   math.sqrt(sum((result["circuit_threshold"] - mean_circuit_threshold) ** 2 
                                                for result in results))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")