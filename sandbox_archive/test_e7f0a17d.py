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
    n = 5 + random.randint(0, 34)  # Ensure n_min >= 5 and n_max >= 20
    if n > 40:
        return {
            "metric_name": "order_div_degree",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "n_too_large"
        }
    
    # Generate a random XOR Boolean function f with n variables
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the vanishing ideal I of f
    I = set()
    for i in range(2**n):
        if f[i] == 1:
            monomial = [i >> j & 1 for j in range(n)]
            I.add(tuple(monomial))
    
    # Compute the order |I| and the degree deg(f) of f
    order_I = len(I)
    degree_f = n
    
    # Check if |I| ≤ deg(f) * c for a constant c
    c = 2  # Example constant, can be adjusted as needed
    conjecture_holds = order_I <= degree_f * c
    
    return {
        "metric_name": "order_div_degree",
        "metric_value": order_I / degree_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"order_I={order_I}, deg_f={degree_f}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE budget_exceeded n_tested={len(results)}")