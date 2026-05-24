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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_hecke_algebra(f):
        n = int(math.log2(len(f)))
        H = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    H[i][j] = 1
        return H
    
    def compute_exponential_depth(f):
        n = int(math.log2(len(f)))
        depth = 0
        while len(f) > 1:
            new_f = []
            for i in range(0, len(f), 2):
                if f[i] == f[i+1]:
                    new_f.append(f[i])
                else:
                    new_f.append(1 - f[i])
            f = new_f
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    H = compute_hecke_algebra(f)
    d = compute_exponential_depth(f)
    
    rho_H = sum(sum(row) for row in H)
    ratio = Fraction(rho_H, 2**d)
    
    return {
        "metric_name": "rho_H / 2^d",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio > 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 1.5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r <= 1.5 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r <= 1.5))]
        print(f"RESULT: FALSIFIED counterexample=\"ratio<=1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")