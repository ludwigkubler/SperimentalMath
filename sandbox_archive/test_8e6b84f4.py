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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def communication_complexity(n):
        # Simplified version of the communication complexity for disjointness function
        return n
    
    def geometric_entropy(g):
        # Simplified version of geometric entropy in terms of genus g
        if g == 0:
            return 0
        return math.log2(2 * g + 1)
    
    n = random.randint(5, 40)
    comm_complexity = communication_complexity(n)
    target_entropy = comm_complexity
    
    for g in range(comm_complexity**2 + 1):
        entropy = geometric_entropy(g)
        if entropy >= target_entropy:
            return {
                "metric_name": "geometric_entropy",
                "metric_value": entropy,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": -1,  # Indicates failure
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": f"No Riemann surface with genus g ≥ {comm_complexity**2} found"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
            61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127
        ]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] >= 0) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] >= 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")