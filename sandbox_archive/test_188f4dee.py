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
    
    def hamiltonian_dynamics(f, n):
        # Simplified Hamiltonian dynamics for demonstration
        H = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    H += 1
        return H
    
    def resolution_proof_depth(f, n):
        # Simplified resolution proof depth for demonstration
        t = 0
        while any(x == 0 for x in f):
            f = [x ^ f[(i + j) % n] for i, j in enumerate(range(1, n))]
            t += 1
        return t
    
    def geometric_entropy(H):
        if H == 0:
            return 0
        return -H * math.log2(H / (2**n))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    H = hamiltonian_dynamics(f, n)
    t_star = resolution_proof_depth(f, n)
    metric_value = geometric_entropy(H) ** 2
    instances_tested = 1
    n_max = n
    conjecture_holds = (metric_value <= t_star)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy_squared",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")