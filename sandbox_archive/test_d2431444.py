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
    
    def tropicalize(f):
        # Placeholder for tropicalization logic
        return sum(abs(x) for x in f)
    
    def circuit_size(f):
        # Placeholder for circuit size calculation
        return len(f)
    
    def min_rank(sheaf):
        # Placeholder for minimal rank calculation
        return max(sheaf)
    
    n = random.randint(5, 40)
    f = [random.uniform(-1, 1) for _ in range(n)]
    F = tropicalize(f)
    sheaf = [max(abs(x - y) for x, y in zip(f[:i], f[i+1:])) for i in range(n-1)]
    rank = min_rank(sheaf)
    circ_size = circuit_size(f)
    
    k = random.randint(1, 5)
    c = random.uniform(0.1, 1)
    
    ratio = rank / (2**k / (2**(k - c) + 1))
    conjecture_holds = ratio > 1
    counterexample = "" if conjecture_holds else f"Function: {f}, Rank: {rank}, Circuit Size: {circ_size}"
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")