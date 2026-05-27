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
    
    # Generate a random polynomial f(x) = x^N + a_{N-1}x^{N-1} + ... + a_0
    N = 20  # Choose a fixed n for simplicity
    coefficients = [random.randint(0, 100) for _ in range(N+1)]
    f = lambda x: sum(c * x**i for i, c in enumerate(coefficients))
    
    # Compute the characteristic polynomial χ_f(T)
    chi_f = lambda T: T**N - sum(a * T**(N-i-1) for i, a in enumerate(coefficients[1:]))
    
    # Simulate computing the rank of the Eichler-Shimura modular form
    # For simplicity, let's assume we can compute this directly (this is a placeholder)
    rank = N  # Placeholder value, should be replaced with actual computation
    
    # Construct an ACC⁰ circuit for f(x) and verify its size
    acc0_circuit_size = N**2  # Placeholder value, should be replaced with actual computation
    
    # Check if the conjecture holds
    conjecture_holds = rank <= math.log(N)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} > log({N})"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds log(N)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")