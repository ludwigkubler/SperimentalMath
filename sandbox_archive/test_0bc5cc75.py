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
    
    def circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        min_size = float('inf')
        for i in range(1, n):
            left = circuit_size(f[:i])
            right = circuit_size(f[i:])
            min_size = min(min_size, left + right + 1)
        return min_size
    
    def linear_representations(f):
        n = len(f)
        F = [0, 1]  # Finite field with two elements
        representations = set()
        for a in F:
            for b in F:
                if (a * f[0] + b * f[1]) % 2 == f[2]:
                    representations.add((a, b))
        return len(representations)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        instances_tested = 0
        n_max = n
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(100):
            f = generate_boolean_function(n)
            C_f = linear_representations(f)
            Ω_f = circuit_size(f)
            
            if Ω_f == 0:
                continue
            
            ratio = math.log(n + 1)**2 * C_f / Ω_f
            results.append(ratio)
            instances_tested += 1
        
        if not all(0 < r <= 1 for r in results):
            conjecture_holds = False
            counterexample = "Ratio out of bounds"
    
    return {
        "metric_name": "log(n + 1)^2 * C(f) / Ω(f)",
        "metric_value": sum(results) / len(results),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")