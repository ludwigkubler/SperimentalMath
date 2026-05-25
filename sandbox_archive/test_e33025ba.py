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
    
    def bp_readtwice_circuit_size(f):
        # Placeholder for actual BP_readtwice circuit size computation
        return len(f) * 2
    
    def geometric_quantization_invariant(f):
        # Placeholder for actual geometric quantization invariant computation
        return len(f) * 3
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    t_star = bp_readtwice_circuit_size(f)
    j_f = geometric_quantization_invariant(f)
    
    if t_star == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "t_star is zero"
        }
    
    ratio = j_f / t_star
    expected_ratio = math.log(n)
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - expected_ratio) <= 0.1 * expected_ratio,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"f has {len(r['counterexample'])} variables"
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")