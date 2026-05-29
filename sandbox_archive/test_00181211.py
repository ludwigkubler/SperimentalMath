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

def generate_xor_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def degree(f):
    n = len(f)
    for i in range(n-1, -1, -1):
        if f[i] != 0:
            return i
    return 0

def vanishing_ideal(f):
    n = len(f)
    I = []
    for i in range(2**n):
        monomial = [int((i >> j) & 1) for j in range(n)]
        if all(f[j] == 0 for j in range(n) if monomial[j] == 1):
            I.append(monomial)
    return I

def order(I):
    return len(I)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_xor_function(n)
    
    deg_f = degree(f)
    I = vanishing_ideal(f)
    order_I = order(I)
    
    return {
        "metric_name": "order/I",
        "metric_value": order_I / deg_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order_I <= deg_f * 2,  # Assuming c = 2 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='order/I > deg(f)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")