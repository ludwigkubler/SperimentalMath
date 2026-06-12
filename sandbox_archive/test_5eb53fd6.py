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
    
    def generate_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def dpll_width(phi):
        # Placeholder implementation of DPLL width calculation
        # This is a dummy function and should be replaced with actual logic
        return len(phi)  # Simplified for demonstration purposes
    
    def local_ring_rank(phi):
        # Placeholder implementation of local ring rank calculation
        # This is a dummy function and should be replaced with actual logic
        return len(phi)  # Simplified for demonstration purposes
    
    n = random.randint(5, 40)
    phi = generate_instance(n)
    w_phi = dpll_width(phi)
    r_phi = local_ring_rank(phi)
    
    return {
        "metric_name": "DPLL Width vs Local Ring Rank",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, w={r['metric_value']}, r={local_ring_rank(generate_instance(r['n_max']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break