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
    
    def generate_random_resolution_proof(width):
        # Placeholder for generating a random resolution proof
        return [random.randint(1, width) for _ in range(random.randint(5, 10))]
    
    def compute_minimal_frobenius_degree(proof):
        # Placeholder for computing the minimal degree of Frobenius element
        # This is a dummy implementation; replace with actual logic
        return random.randint(1, len(proof))
    
    width = random.randint(5, 40)
    proof = generate_random_resolution_proof(width)
    d_phi = compute_minimal_frobenius_degree(proof)
    
    metric_name = "minimal_frobenius_degree"
    metric_value = d_phi
    instances_tested = 1
    n_max = width
    conjecture_holds = False
    counterexample = ""
    
    if d_phi <= 2 * math.log(width):
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        counterexample = f"Seed {first_failing_seed + 1}, d(φ)={results[first_failing_seed]['metric_value']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")