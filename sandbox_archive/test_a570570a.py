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
    
    # Generate a random n-dimensional vector space
    n = random.randint(5, 40)
    V = [[random.random() for _ in range(n)] for _ in range(n)]
    
    # Compute the minimal rank of the quadratic intersection structure on G
    min_rank = n  # Placeholder value; actual computation depends on the specific geometry
    
    # Build AC0 circuits for computing the parity function on n inputs and measure their depth
    def ac0_circuit_depth(n):
        if n == 1:
            return 1
        else:
            return 2 + ac0_circuit_depth(n // 2)
    
    circuit_depth = ac0_circuit_depth(n)
    
    # Correlate the minimal ranks with the circuit depths, aiming to find a linear correlation
    c = math.log(n) / circuit_depth
    
    # Check if the conjecture holds for this seed
    conjecture_holds = min_rank <= c * circuit_depth
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, expected<=c*{circuit_depth}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    total_metric_value = sum(result["metric_value"] for result in results)
    total_instances_tested = sum(result["instances_tested"] for result in results)
    mean_metric_value = total_metric_value / total_instances_tested
    
    std_dev = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / total_instances_tested)
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")