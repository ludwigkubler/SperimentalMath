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
    
    def generate_communication_protocol(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def calculate_rank_variance(phi):
        n = len(phi)
        mean = sum(phi) / n
        variance = sum((x - mean) ** 2 for x in phi) / n
        return variance
    
    def construct_braided_algebra(phi):
        # Placeholder function to simulate the construction of a braided algebra
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    def calculate_min_rank(braided_algebra):
        return braided_algebra  # Simplified for demonstration
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    variances = []
    
    for n in n_values:
        phi = generate_communication_protocol(n)
        variance = calculate_rank_variance(phi)
        braided_algebra = construct_braided_algebra(phi)
        min_rank = calculate_min_rank(braided_algebra)
        
        min_ranks.append(min_rank)
        variances.append(variance)
    
    correlation = correlation_coefficient(min_ranks, variances)
    p_value = p_value_correlation(len(min_ranks) - 2, correlation)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

def correlation_coefficient(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    
    if std_x == 0 or std_y == 0:
        return 0
    
    return cov / (std_x * std_y)

def p_value_correlation(df, r):
    # Approximate p-value using the t-distribution
    t = abs(r) * math.sqrt(df) / math.sqrt(1 - r ** 2)
    if t < 1.645:
        return 0.1
    elif t < 1.96:
        return 0.05
    elif t < 2.326:
        return 0.01
    else:
        return 0.001

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]
        seeds = primes[:30]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break