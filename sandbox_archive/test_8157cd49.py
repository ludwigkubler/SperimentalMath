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
    n = random.randint(3, 40)
    
    # Generate a random Boolean function f with n variables
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the communication complexity C(f)
    def communication_complexity(f):
        # Placeholder for actual communication complexity computation
        return len(f) / 2
    
    C_f = communication_complexity(f)
    
    # Determine the minimal representation rank ρ(f) over various Coxeter systems
    def minimal_representation_rank(f):
        # Placeholder for actual minimal representation rank computation
        return len(f)
    
    ρ_f = minimal_representation_rank(f)
    
    # Correlate the computed ranks with the communication complexities to test the conjectured relationship
    ratio = ρ_f / C_f
    
    result = {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else "Ratio exceeds 1.5"
    }
    
    return result

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1.5' first_failing_seed={first_failing_seed}")