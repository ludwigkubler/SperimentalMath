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
    
    def circuit_depth(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        depth = 0
        while len(f) > 1:
            f = [f[i] ^ f[i+1] for i in range(0, len(f), 2)]
            depth += 1
        return depth
    
    def generality(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        # Simplistic heuristic: number of unique values in the function
        return len(set(f))
    
    N = random.randint(5, 40)
    f = generate_boolean_function(N)
    depth = circuit_depth(f)
    gen = generality(f)
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": N,
        "conjecture_holds": depth <= 2 * gen,  # Example constant
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")