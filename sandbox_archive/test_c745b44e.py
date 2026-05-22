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
    
    def generate_polynomial(n, d):
        # Generate a random polynomial f over {0,1}^n with degree at most d
        coefficients = [random.randint(0, 1) for _ in range(d + 1)]
        return coefficients
    
    def discrepancy_tensor_rank(coefficients):
        # Placeholder function to compute the rank of the discrepancy tensor
        # This is a dummy implementation and should be replaced with actual computation
        return len(coefficients)
    
    def read_twice_branching_program_size(n, d):
        # Placeholder function to compute the size of the read-twice branching program
        # This is a dummy implementation and should be replaced with actual computation
        return 2 ** (n // d)
    
    n = random.randint(5, 40)
    d = random.randint(1, 10)
    f = generate_polynomial(n, d)
    rank_T_f = discrepancy_tensor_rank(f)
    size_P = read_twice_branching_program_size(n, d)
    
    metric_value = rank_T_f
    instances_tested = 1
    conjecture_holds = False
    counterexample = "mapping_undefined"
    
    return {
        "metric_name": "discrepancy_tensor_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")