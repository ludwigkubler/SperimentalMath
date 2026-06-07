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
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        # Placeholder implementation of rcv(f)
        return sum(f[i] != f[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
    
    def minimal_local_induction_dimension(f):
        n = int(math.log2(len(f)))
        # Placeholder implementation of mild(f)
        return sum(1 for x in f if x == 0 or x == 1) / len(f)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        mild_f = minimal_local_induction_dimension(f)
        rcv_f = communication_complexity_rank_variance(f)
        results.append((mild_f, rcv_f))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mild_values = [r[0] for r in results]
    rcv_values = [r[1] for r in results]
    
    mean_mild = sum(mild_values) / len(mild_values)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    covariance = sum((mild_values[i] - mean_mild) * (rcv_values[i] - mean_rcv) for i in range(len(results))) / len(results)
    variance_mild = sum((mild_values[i] - mean_mild)**2 for i in range(len(results))) / len(results)
    variance_rcv = sum((rcv_values[i] - mean_rcv)**2 for i in range(len(results))) / len(results)
    
    pearson_r = covariance / (math.sqrt(variance_mild) * math.sqrt(variance_rcv))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_r,
        "instances_tested": 30,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": pearson_r >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")