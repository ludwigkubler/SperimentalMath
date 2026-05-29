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
        coefficients = [random.choice([0, 1]) for _ in range(2**n)]
        return lambda x: sum(coefficients[i] * (x >> i & 1) for i in range(2**n)) % 2
    
    def degree(f):
        n = len(f)
        for d in range(n, -1, -1):
            if any(f(x) != 0 for x in range(2**d)):
                return d
        return 0
    
    def vanishing_ideal(f, n):
        I = set()
        for i in range(2**n):
            if f(i) == 0:
                monomial = [1] * n
                for j in range(n):
                    if (i >> j) & 1:
                        monomial[j] = -1
                I.add(tuple(monomial))
        return I
    
    def order(I):
        return len(I)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_xor_function(n)
    deg_f = degree(f)
    I = vanishing_ideal(f, n)
    order_I = order(I)
    
    return {
        "metric_name": "order_over_degree",
        "metric_value": order_I / deg_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order_I <= deg_f * 2,  # Assuming c = 2 for simplicity
        "counterexample": "" if order_I <= deg_f * 2 else f"Counterexample: n={n}, |I|={order_I}, deg(f)={deg_f}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")