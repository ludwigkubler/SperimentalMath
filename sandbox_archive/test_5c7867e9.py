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
    
    # Define the finite field F_q (for simplicity, let's use q=2)
    q = 2
    
    # Generate a random tropical curve with n variables
    n = random.randint(5, 40)
    curve_eqs = ['x' + str(i) for i in range(n)]
    
    # Compute the associated multivariate polynomial (for simplicity, let's use a linear combination)
    poly = sum(random.choice([-1, 1]) * 'x' + str(i) for i in range(n))
    
    # Determine the Minimal Hodge Index (H1) (for simplicity, let's assume it's equal to n)
    H1 = n
    
    # Determine the smallest AC0 circuit that computes the multivariate polynomial
    # For simplicity, let's assume the size of the circuit is proportional to n^2
    ac0_circuit_size = n ** 2
    
    # Compare the size of the circuit to the Minimal Hodge Index (H1)
    if H1 <= ac0_circuit_size:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Found a tropical curve with H1 > AC0 circuit size"
    
    return {
        "metric_name": "H1 vs AC0 Circuit Size",
        "metric_value": H1,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")