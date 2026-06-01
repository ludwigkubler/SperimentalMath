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
    
    def generate_sat_instance(n):
        clauses = set()
        for _ in range(n):
            clause = tuple(random.sample(range(1, n+1), 2))
            clauses.add(clause)
        return clauses
    
    def polynomial_modulo(polynomial, p):
        return [x % p for x in polynomial]
    
    def modular_function_rank(poly, p):
        poly = polynomial_modulo(poly, p)
        degree = len(poly) - 1
        if degree == 0:
            return 0
        rank = 1
        for i in range(1, degree + 1):
            coeff = poly[i]
            if coeff != 0:
                rank += 1
        return rank
    
    def unique_clauses(clauses):
        return len(clauses)
    
    p = 101  # Prime number for modulo operation
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        mfr_sum = 0
        unique_clauses_sum = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            poly = [1] + [0] * (n - 1)  # Polynomial representing the instance
            for clause in clauses:
                x, y = clause
                poly[x-1] += 1
                poly[y-1] += 1
            
            mfr = modular_function_rank(poly, p)
            unique_clauses_count = unique_clauses(clauses)
            
            mfr_sum += mfr
            unique_clauses_sum += unique_clauses_count
            instances_tested += 1
        
        mean_mfr = mfr_sum / instances_tested
        mean_unique_clauses = unique_clauses_sum / instances_tested
        
        results.append({
            "n": n,
            "mean_mfr": mean_mfr,
            "mean_unique_clauses": mean_unique_clauses
        })
    
    correlation_coefficient = 0
    if len(results) > 1:
        x_mean = sum(result["mean_unique_clauses"] for result in results) / len(results)
        y_mean = sum(result["mean_mfr"] for result in results) / len(results)
        
        numerator = sum((result["mean_unique_clauses"] - x_mean) * (result["mean_mfr"] - y_mean) for result in results)
        denominator = math.sqrt(sum((result["mean_unique_clauses"] - x_mean) ** 2 for result in results)) * math.sqrt(sum((result["mean_mfr"] - y_mean) ** 2 for result in results))
        
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient - 1) <= 0.1,
        "counterexample": "" if abs(correlation_coefficient - 1) <= 0.1 else f"Correlation coefficient {correlation_coefficient} is not within ±10% of 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 101, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")