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
    
    # Khinchin's constant
    pi_0 = 2.718281828459045
    
    # Generate a random boolean circuit with n inputs and output size m
    n = random.randint(5, 40)
    m = random.randint(1, 2)
    
    # Calculate the entropy H(C) of the circuit using Shannon's formula
    # For simplicity, we assume each gate has an equal probability of being true or false
    # This is a very simplified model and not representative of real circuits
    entropy_C = -m * (math.log(m / 2**n, 2) + (1 - m) * math.log((1 - m) / (2**(n-1)), 2))
    
    # Calculate the difference |H(C) - 2/H(π_0)|
    diff = abs(entropy_C - 2 / pi_0)
    
    return {
        "metric_name": "entropy_difference",
        "metric_value": diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": diff <= 1 / pi_0,
        "counterexample": "" if diff <= 1 / pi_0 else f"Entropy difference {diff} exceeds threshold"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    if all("metric_value" in r for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE missing_metric_value")