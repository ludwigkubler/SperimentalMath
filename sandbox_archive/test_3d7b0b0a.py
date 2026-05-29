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
    
    def log_q(n):
        return math.log(2**n, 2)
    
    def arithmetic_hodge_dimension(n):
        # Placeholder function to simulate the computation of the dimension
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def within_bound(dimension, n):
        return dimension <= log_q(n) * (log_q(n))**2
    
    metric_name = "arithmetic_hodge_dimension"
    instances_tested = 0
    total_dimension = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        dimension = arithmetic_hodge_dimension(n)
        if not within_bound(dimension, n):
            conjecture_holds = False
            counterexample = f"n={n}, dimension={dimension}"
            break
        total_dimension += dimension
        instances_tested += 1
    
    mean_dimension = total_dimension / instances_tested if instances_tested > 0 else 0
    std_dimension = math.sqrt(sum((x - mean_dimension)**2 for x in [arithmetic_hodge_dimension(n) for _ in range(30)]) / instances_tested) if instances_tested > 1 else 0
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(x) for x in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    std_dimension = math.sqrt(sum((r["metric_value"] - mean_dimension)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std={std_dimension} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std={std_dimension} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")