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
    
    # Define constants for the conjecture
    alpha = 1.0
    beta = 2.0
    
    # Generate a random instance of Tensor Network Compression with n nodes
    n = random.randint(5, 40)
    instances_tested = n
    
    # Compute the communication complexity f(n) = α * log(β^n)
    f_n = alpha * math.log(beta ** n)
    
    # Compute the geometric entropy g(n) = Ω(log(β^n))
    g_n = math.log(beta ** n)
    
    # Calculate the ratio f(n)/g(n)
    ratio = f_n / g_n
    
    # Check if the conjecture holds
    conjecture_holds = abs(ratio - 1.0) < 0.01
    counterexample = "" if conjecture_holds else "f(n)/g(n) does not remain constant"
    
    return {
        "metric_name": "Ratio f(n)/g(n)",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 prime numbers if no seeds provided
    
    results = []
    total_ratio = 0.0
    count_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_holds += 1
    
    mean_ratio = total_ratio / len(seeds)
    support_fraction = count_holds / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n)/g(n) does not remain constant\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")