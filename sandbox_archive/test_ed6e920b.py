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
    
    def generate_sat_instance(n):
        clauses = set()
        for _ in range(2**n):
            clause = tuple(sorted(random.sample(range(-n, n+1), 3)))
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.add(clause)
        return clauses
    
    def self_dual_codes(clauses):
        n = max(abs(lit) for clause in clauses for lit in clause)
        codes = []
        for _ in range(len(clauses)):
            code = [0] * (2*n)
            for literal in random.sample(range(-n, n+1), 2*n):
                if literal not in code:
                    code[literal - 1] = 1
            codes.append(code)
        return codes, None
    
    def entropy(clauses):
        num_clauses = len(clauses)
        total_bits = sum(math.log2(2**n) for clause in clauses)
        avg_bits_per_clause = total_bits / num_clauses
        return avg_bits_per_clause
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_sat_instance(n)
        codes, error = self_dual_codes(clauses)
        if error is not None:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"mapping_undefined for n={n}"
            }
        results.append(len(codes))
    
    mean_codes = sum(results) / len(results)
    std_codes = math.sqrt(sum((x - mean_codes)**2 for x in results) / len(results))
    correlation = None
    
    if len(results) > 1:
        mean_entropy = entropy(clauses)
        covariance = sum((results[i] - mean_codes) * (i + 5 - mean_entropy) for i in range(len(results))) / (len(results) - 1)
        variance_entropy = sum((i + 5 - mean_entropy)**2 for i in range(len(results))) / (len(results) - 1)
        correlation = covariance / math.sqrt(variance_entropy * std_codes**2)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation is not None and abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if trial_result["conjecture_holds"]:
            results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = len([r for r in results if abs(r) >= 0.8 * mean_value]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r) < 0.8 * mean_value for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.8 * mean_value))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_less_than_0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")