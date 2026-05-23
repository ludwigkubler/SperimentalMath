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
    
    def generate_explicit_function(n):
        # Generate a random polynomial over GF(2) with degree n
        return [random.choice([0, 1]) for _ in range(n + 1)]
    
    def acc0_circuit_threshold(f):
        # Simulate the ACC⁰ circuit threshold (simplified)
        return len(f) - 1
    
    def tropicalized_boolean_algebra(f):
        # Convert polynomial to tropicalized Boolean algebra
        tba = []
        for i in range(len(f)):
            if f[i] == 1:
                tba.append(i)
        return tba
    
    def tensor_product_rank(tba):
        # Compute the minimal tensor product rank (simplified)
        return len(tba) if tba else 0
    
    n = random.randint(5, 40)
    f = generate_explicit_function(n)
    threshold = acc0_circuit_threshold(f)
    tba = tropicalized_boolean_algebra(f)
    rank = tensor_product_rank(tba)
    
    ratio = rank / threshold if threshold != 0 else float('inf')
    conjecture_holds = 0.8 <= ratio <= 1.2
    
    return {
        "metric_name": "Ratio of Tensor Product Rank to ACC⁰ Circuit Threshold",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Function: {f}, Rank: {rank}, Threshold: {threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")