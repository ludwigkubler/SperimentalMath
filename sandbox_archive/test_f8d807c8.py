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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        rank = 0
        for i in range(n):
            if any(f[j] == f[j ^ (1 << i)] for j in range(2**(n-1))):
                rank += 1
        return rank
    
    def minimal_order_hecke_group(f):
        n = int(math.log2(len(f)))
        order = 0
        for i in range(n):
            if any(f[j] == f[j ^ (1 << i)] for j in range(2**(n-1))):
                order += 1
        return order
    
    instances_tested = 0
    n_max = 0
    total_order = 0
    total_rank = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        order = minimal_order_hecke_group(f)
        
        total_order += order
        total_rank += rank
        instances_tested += 1
    
    mean_order = Fraction(total_order, instances_tested)
    mean_rank = Fraction(total_rank, instances_tested)
    
    correlation_coefficient = (instances_tested * mean_order * mean_rank - 
                               total_order * total_rank) / (
                                   math.sqrt((instances_tested * mean_order**2 - total_order**2) *
                                             (instances_tested * mean_rank**2 - total_rank**2)))
    
    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {{\"seed\": {}, \"metric_name\": \"Pearson Correlation Coefficient\", \"metric_value\": {:.4f}, \"instances_tested\": {}, \"n_max\": {}, \"conjecture_holds\": {}, \"counterexample\": \"{}\"}}".format(
            seed, result["metric_value"], result["instances_tested"], result["n_max"], result["conjecture_holds"], result["counterexample"]
        ))
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_metric, std_metric, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_metric, std_metric, support_fraction))
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))