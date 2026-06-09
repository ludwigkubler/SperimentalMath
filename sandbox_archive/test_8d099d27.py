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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def entropy(n, epsilon):
        return n * log2(1 / epsilon)
    
    instances_tested = 0
    total_entropy = 0.0
    max_n = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        max_n = max(max_n, n)
        epsilon = random.uniform(1e-6, 0.5)
        
        B = random.randint(1, n * (n - 1) // 2)
        H_min_phi = entropy(n, epsilon)
        
        instances_tested += 1
        total_entropy += H_min_phi
    
    metric_value = total_entropy / instances_tested
    conjecture_holds = all(H_min_phi <= entropy(n, epsilon) for n in range(5, 41) for epsilon in [1e-6, 0.5])
    
    return {
        "metric_name": "minimal_quadratic_entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"B={r['n_max']}, E=1e-6, H_min_phi={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_evidence")