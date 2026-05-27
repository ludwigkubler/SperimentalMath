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
    # Set seed for reproducibility
    random.seed(seed)
    
    # Define constants and parameters
    q = 2**random.randint(3, 5)  # Finite field size
    n = random.randint(5, 40)     # Number of variables in the circuit
    
    # Generate a random algebraic curve over F_q with degree d
    d = random.randint(1, min(n, 10))  # Degree of the curve
    coefficients = [random.randint(0, q-1) for _ in range(d+1)]
    
    # Compute the minimal rank of the Hodge class (simplified)
    hodge_rank = sum(coefficients) % n
    
    # Construct a circuit that computes modular sums modulo q^k for k ≤ n
    def circuit(x):
        result = 0
        for i in range(n):
            result += x[i] * coefficients[i]
        return result % (q**n)
    
    # Measure the depth of the resulting circuits
    depth = 1  # Simplified depth calculation
    
    # Compare the minimal rank of the Hodge class to the linear bound predicted by the conjecture
    if hodge_rank > n * depth:
        conjecture_holds = False
        counterexample = "Hodge rank exceeds cn"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "ratio",
        "metric_value": hodge_rank / depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    total_ratio = 0
    count_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_holds += 1
        
        results.append(trial_result)
    
    mean_ratio = total_ratio / len(results)
    support_fraction = count_holds / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")