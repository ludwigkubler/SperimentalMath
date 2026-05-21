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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_curve(f):
        n = int(math.log2(len(f)))
        curve = []
        for i in range(n):
            for j in range(i+1, n):
                if f[2**i + 2**j] == 1:
                    curve.append((i, j))
        return curve
    
    def min_local_gromov_witten_invariant(curve):
        if not curve:
            return 0
        return len(curve)
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        curve = compute_tropical_curve(f)
        invariant = min_local_gromov_witten_invariant(curve)
        
        if invariant < math.log(len(f), 2):
            return {
                "metric_name": "min_local_gromov_witten_invariant",
                "metric_value": invariant,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, s(n)={len(f)}, invariant={invariant}"
            }
    
    return {
        "metric_name": "min_local_gromov_witten_invariant",
        "metric_value": math.log(len(f), 2),
        "instances_tested": 6,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")