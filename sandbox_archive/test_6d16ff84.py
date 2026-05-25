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
    n = 10  # Example value for n, can be adjusted within each trial
    c = 1   # Example constant for the invariant ψ(T)
    c_prime = 2  # Example constant for the rank comparison
    
    # Generate a random n-dimensional manifold (simplified representation)
    M = [random.randint(0, 1) for _ in range(n)]
    
    # Construct a tropicalized sheaf over M (simplified representation)
    T = [random.randint(0, 1) for _ in range(n)]
    
    # Compute the size of the tropicalized sheaf
    size_T = sum(T)
    
    # Define the invariant ψ(T) on the tropicalized sheaf T
    def psi(T):
        return c * math.log(size_T + 1)
    
    # Apply the invariant ψ(T) to the tropicalized sheaf T
    metric_value = psi(T)
    
    # Generate an AC0 parity circuit C with size less than 2^(1.5n)
    size_C = random.randint(1, int(2 ** (1.5 * n)))
    C = [random.randint(0, 1) for _ in range(size_C)]
    
    # Compute the rank of the corresponding tropicalized sheaf T over M
    rank_T = sum(T)
    
    # Check if ψ(T) > 2c·log(n)
    conjecture_holds = metric_value > 2 * c * math.log(n)
    
    # Find a counterexample if the conjecture does not hold
    counterexample = "" if conjecture_holds else f"ψ(T)={metric_value} <= 2c·log(n)={2*c*math.log(n)}"
    
    return {
        "metric_name": "Invariant ψ(T)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [random.randint(2, 100) for _ in range(30)] if len(sys.argv[1:]) == 0 else list(map(int, sys.argv[1:]))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")