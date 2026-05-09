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
    
    def gowers_u3_norm(f, n):
        # Compute Gowers U^3 norm using discrete Fourier transform
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    F[i][j] += f[(i, j, k)] * math.exp(-2j * math.pi * (i * k + j * k) / n)
        norm = sum(abs(F[i][j]) ** 4 for i in range(n + 1) for j in range(n + 1)) ** 0.25
        return norm
    
    def ip2_function(x):
        # IP_2 function: f(x, y) = x * y (mod n)
        n = len(x)
        f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                f[i][j] = (i * j) % n
        return f
    
    def generate_read_twice_bp(n, S):
        # Generate a random read-twice BP with size S
        bp = {}
        for _ in range(S):
            x1 = random.randint(0, n - 1)
            x2 = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            if (x1, x2) not in bp:
                bp[(x1, x2)] = []
            bp[(x1, x2)].append(y)
        return bp
    
    n = 40
    S = 100
    
    # Generate read-twice BP and compute U^3 norm
    bp = generate_read_twice_bp(n, S)
    f_bp = {(i, j, k): random.randint(0, 1) for i in range(n) for j in range(n) for k in range(n)}
    u3_norm_bp = gowers_u3_norm(f_bp, n)
    
    # Compute IP_2 function and its U^3 norm
    f_ip2 = ip2_function([i for i in range(n)])
    u3_norm_ip2 = gowers_u3_norm(f_ip2, n)
    
    return {
        "metric_name": "Gowers U^3 norm",
        "metric_value": max(u3_norm_bp, u3_norm_ip2),
        "instances_tested": 1,
        "conjecture_holds": u3_norm_bp <= math.log(S) and u3_norm_ip2 >= n / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")