# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        return [random.randint(1, 100) for _ in range(n)]
    
    def compute_minimal_norm(instance):
        n = len(instance)
        norm = sum(x**2 for x in instance) / n
        return Fraction(norm).limit_denominator()
    
    def compute_growth_rate(instance):
        n = len(instance)
        growth_rate = (sum(instance[:i]) for i in range(1, n+1))
        return max(growth_rate)
    
    instances_tested = 0
    total_norm = 0
    total_growth_rate = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        instance = generate_instance(n)
        norm = compute_minimal_norm(instance)
        growth_rate = compute_growth_rate(instance)
        
        total_norm += norm
        total_growth_rate += growth_rate
        instances_tested += 1
    
    mean_norm = Fraction(total_norm).limit_denominator() / instances_tested
    mean_growth_rate = total_growth_rate / instances_tested
    
    correlation_coefficient = (instances_tested * sum(norm * growth_rate for norm, growth_rate in zip(map(compute_minimal_norm, [generate_instance(n) for n in range(5, 41)]), map(compute_growth_rate, [generate_instance(n) for n in range(5, 41)]))) - instances_tested * mean_norm * mean_growth_rate) / (instances_tested * sum((norm - mean_norm)**2 for norm in map(compute_minimal_norm, [generate_instance(n) for n in range(5, 41)])) * sum((growth_rate - mean_growth_rate)**2 for growth_rate in map(compute_growth_rate, [generate_instance(n) for n in range(5, 41)])))**0.5
    
    if correlation_coefficient < 0.5 or correlation_coefficient > Fraction(16, 9):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": ""
        }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 or r["metric_value"] > Fraction(16, 9) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")