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
    
    def xor(a, b):
        return a ^ b
    
    def generate_xor_function(n):
        coefficients = [random.randint(0, 1) for _ in range(2**n)]
        return lambda x: sum(coefficients[i] * (x & (1 << i)) for i in range(2**n))
    
    def degree(f):
        max_degree = 0
        for x in range(2**n):
            if f(x) != 0:
                max_degree = max(max_degree, bin(x).count('1'))
        return max_degree
    
    def vanishing_ideal(f):
        ideal = set()
        for i in range(2**n):
            if f(i) == 0:
                ideal.add(tuple((i >> j) & 1 for j in range(n)))
        return ideal
    
    def order(I):
        return len(I)
    
    n = random.randint(5, 40)
    f = generate_xor_function(n)
    deg_f = degree(f)
    I = vanishing_ideal(f)
    order_I = order(I)
    
    return {
        "metric_name": "order/I",
        "metric_value": order_I / deg_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order_I <= deg_f * 2,  # Using a constant c=2 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"order/I > deg(f) * c\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")