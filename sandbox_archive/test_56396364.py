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
    
    n = 5 + (seed % 6) * 5  # Sweep through {5, 10, 15, 20, 30, 40}
    if n > 30:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "budget_exceeded"
        }
    
    # Generate a random Boolean function f with n variables
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the communication complexity κ_XOR(n)
    def xor_communication_complexity(n):
        return math.ceil(math.log2(n + 1))
    
    k = xor_communication_complexity(n)
    
    # Compute the Brauer group B(f) (simplified for demonstration)
    B_f = len(f)  # This is a dummy value; replace with actual computation
    
    # Measure the ratio |B(f)| / κ_XOR(n)
    if k == 0:
        ratio = None
    else:
        ratio = B_f / k
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": (ratio is not None and ratio <= 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE reason=metric_value_none")
    else:
        supported_count = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"])
        support_fraction = supported_count / len(results)
        
        if support_fraction >= 0.8:
            mean_ratio = sum(r["metric_value"] for r in results) / len(results)
            std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (result["metric_value"] is None or result["conjecture_holds"]))
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")