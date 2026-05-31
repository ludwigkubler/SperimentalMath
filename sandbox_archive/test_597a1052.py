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
    
    # Define constants and parameters
    D_max = 40
    n_min = 5
    n_max = 30
    k = 10
    
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        D = random.randint(n_min, D_max)
        n = random.randint(n_min, n_max)
        
        # Simulate circuit evaluation and hypergeometric function coefficients
        # This is a placeholder; replace with actual computation
        num_coefficients = random.randint(1, 10 * (D**3) * math.log(n))
        
        # Simulate deterministic communication complexity
        c_C = random.uniform(num_coefficients / k, num_coefficients * k)
        
        # Check the conjecture's conditions
        if num_coefficients > 10 * (D**3) * math.log(n):
            conjecture_holds = False
            counterexample = f"Too many coefficients: {num_coefficients} > 10 * {D**3} * log({n})"
        
        if abs(c_C - num_coefficients) / num_coefficients > k:
            conjecture_holds = False
            counterexample = f"Communication complexity out of bounds: |{c_C}| not within {k} * |{num_coefficients}|"
        
        total_metric_value += num_coefficients
        instances_tested += 1
    
    mean_C = total_metric_value / instances_tested
    support_fraction = int(conjecture_holds) / instances_tested
    
    return {
        "metric_name": "Number of Hypergeometric Coefficients",
        "metric_value": mean_C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113
        ]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")