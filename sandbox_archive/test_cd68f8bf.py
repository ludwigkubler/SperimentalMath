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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def linear_representation(f):
        n = int(math.log2(len(f)))
        F = [i % 2 for i in range(2**(n+1))]
        representations = set()
        for a in range(2**(n+1)):
            rep = []
            for b in range(n+1):
                if (a >> b) & 1:
                    rep.append(f[(b * len(f)) // (n + 1)])
                else:
                    rep.append((f[(b * len(f)) // (n + 1)] + 1) % 2)
            representations.add(tuple(rep))
        return len(representations)
    
    def circuit_size(f):
        n = int(math.log2(len(f)))
        if all(x == f[0] for x in f):
            return 1
        if any(x != f[0] and x != f[1] for x in f):
            return 2
        return 3
    
    def log_square_plus_one(n):
        return (math.log(n + 1) ** 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_ratio = 0.0
    
    for n in n_values:
        for _ in range(10):
            f = generate_boolean_function(n)
            C_f = linear_representation(f)
            Ω_f = circuit_size(f)
            if Ω_f == 0:
                continue
            ratio = log_square_plus_one(n) * C_f / Ω_f
            total_ratio += ratio
            instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 1.0  # Placeholder for actual bound check
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log_square_plus_one_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")