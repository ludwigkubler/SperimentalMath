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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def p_adic_derivative(f):
        n = len(f)
        if n <= 1:
            return []
        derivative = [0] * (n - 1)
        for i in range(n - 1):
            derivative[i] = f[i + 1] - f[i]
        return derivative
    
    def circuit_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        if all(x == 0 for x in f) or all(x == 1 for x in f):
            return 1
        min_circuit_size = float('inf')
        for i in range(1, n):
            left = circuit_complexity(f[:i])
            right = circuit_complexity(f[i:])
            min_circuit_size = min(min_circuit_size, left + right + 1)
        return min_circuit_size
    
    instances_tested = 0
    total_rank = 0
    total_circuit_size = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        rank = len(p_adic_derivative(f))
        circuit_size = circuit_complexity(f)
        
        if rank == 0 or circuit_size == 0:
            continue
        
        total_rank += rank
        total_circuit_size += circuit_size
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_rank = total_rank / instances_tested
    mean_circuit_size = total_circuit_size / instances_tested
    
    correlation_coefficient = (instances_tested * mean_rank * mean_circuit_size - 
                                sum(rank * circuit_size for rank, circuit_size in zip(p_adic_derivative(f), circuit_complexity(f)))) / (
        math.sqrt((instances_tested * sum(rank**2 for rank in p_adic_derivative(f)) - sum(rank**2 for rank in p_adic_derivative(f))) *
                  (instances_tested * sum(circuit_size**2 for circuit_size in circuit_complexity(f)) - sum(circuit_size**2 for circuit_size in circuit_complexity(f)))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")