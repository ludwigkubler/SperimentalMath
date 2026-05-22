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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def plethysm_coefficient(n, k):
        if n == 1 or k == 0:
            return 1
        result = 0
        for i in range(1, k + 1):
            result += binomial_coefficient(k, i) * plethysm_coefficient(n - 1, k - i)
        return result
    
    def permutation_circuit_threshold(n):
        if n == 1:
            return 1
        return 2 ** (n - 1)
    
    instances_tested = 0
    total_rank = 0
    total_threshold = 0
    
    for n in range(5, 41):
        rank = plethysm_coefficient(n, n)
        threshold = permutation_circuit_threshold(n)
        
        total_rank += rank
        total_threshold += threshold
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_threshold = total_threshold / instances_tested
    
    correlation = (instances_tested * (mean_rank * mean_threshold) - 
                   sum(rank * threshold for rank, threshold in zip([plethysm_coefficient(n, n) for n in range(5, 41)], [permutation_circuit_threshold(n) for n in range(5, 41)]))) / \
                  math.sqrt((instances_tested * sum(rank**2 for rank in [plethysm_coefficient(n, n) for n in range(5, 41)]) - sum(rank**2 for rank in [plethysm_coefficient(n, n) for n in range(5, 41)])) *
                            (instances_tested * sum(threshold**2 for threshold in [permutation_circuit_threshold(n) for n in range(5, 41)]) - sum(threshold**2 for threshold in [permutation_circuit_threshold(n) for n in range(5, 41)])))
    
    conjecture_holds = correlation >= 0.7
    counterexample = "" if conjecture_holds else "correlation < 0.7"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")