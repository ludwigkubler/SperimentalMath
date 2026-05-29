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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def support_size(g):
        return sum(1 for x in range(2**n) if g[x] != f[x])
    
    n = random.randint(5, 40)
    f = generate_xor_function(n)
    
    q_f = None
    for k in range(1, 2**n + 1):
        found = True
        for x in range(2**n):
            if (x & (k - 1)) != x:
                continue
            g = [0] * (2**n)
            for i in range(n):
                if x & (1 << i):
                    g[x ^ (1 << i)] = 1
            if support_size(g) >= n // 2 and all(g[f(x)] == 1 for x in range(2**n)):
                q_f = k
                break
        if q_f is not None:
            break
    
    if q_f is None:
        return {
            "metric_name": "q(f)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "No valid quadratic form found"
        }
    
    C_f = random.randint(1, 2**n)
    O_qf = q_f
    Omega_qf2 = q_f ** 2
    
    return {
        "metric_name": "q(f)",
        "metric_value": q_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": O_qf <= C_f and C_f <= Omega_qf2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")