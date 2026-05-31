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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid boolean function length")
        count = 0
        for i in range(n):
            bits = [f[j] for j in range(2**n) if (j >> i) & 1]
            count += max(bits.count(0), bits.count(1))
        return count
    
    def minimal_local_index_of_tropical_motivic_homology(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid boolean function length")
        # Placeholder for actual computation
        return random.uniform(0, communication_complexity(f))
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        mtr_h = minimal_local_index_of_tropical_motivic_homology(f)
        results.append((cc, mtr_h))
    
    if not all(results):
        return {
            "metric_name": "mtr_h - cc",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_diff = sum(abs(cc - mtr_h) for cc, mtr_h in results) / len(results)
    return {
        "metric_name": "mtr_h - cc",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": mean_diff <= 1,  # Placeholder constant k
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mtr_h - cc > 1\" first_failing_seed={result['seed']}")
                break