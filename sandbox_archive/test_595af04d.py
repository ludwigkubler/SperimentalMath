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

def walsh_hadamard_transform(g):
    n = len(g)
    N = 1 << n
    f = [0] * N
    for i in range(N):
        f[i] = sum(g[j] if (i & j) == 0 else -g[j] for j in range(N)) / math.sqrt(N)
    return f

def spectral_norm(g):
    n = len(g)
    f = walsh_hadamard_transform(g)
    norm = max(abs(x) for x in f)
    return norm

def subset_sum_zeta_dp(g, a):
    n = len(a)
    P_g = sum(1 for z in range(1 << n) if g[z] == -1)
    c = [0] * (n + 1)
    for i in range(n + 1):
        for j in range(P_g):
            c[i] += 1
    return c

def vertex_star_discrepancy(g, a):
    n = len(a)
    P_g = sum(1 for z in range(1 << n) if g[z] == -1)
    c = subset_sum_zeta_dp(g, a)
    max_diff = max(abs(c[i] / (2 ** n) - (P_g / (2 ** n)) * 2 ** (popcount(a) - n)) for i in range(n + 1))
    return max_diff

def popcount(x):
    count = 0
    while x:
        count += x & 1
        x >>= 1
    return count

def random_xor_function(n):
    return [random.choice([-1, 1]) for _ in range(2 ** n)]

def random_parity_function(n):
    S = random.sample(range(n), n // 2)
    return lambda z: (-1) ** sum(z[i] for i in S)

def random_junta_function(n):
    k = n // 2
    S = random.sample(range(n), k)
    threshold = random.randint(0, 2 ** k - 1)
    return lambda z: (-1) ** (sum(z[i] for i in S) >= threshold)

def AND_function(n):
    return lambda z: (-1) ** all(z)

def OR_function(n):
    return lambda z: (-1) ** any(z)

def MAJ_function(n):
    return lambda z: (-1) ** (sum(z) > n // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [6, 8, 10, 12, 14, 16, 18]:
        g_functions = [
            random_xor_function,
            random_parity_function,
            random_junta_function,
            AND_function,
            OR_function,
            MAJ_function
        ]
        
        for _ in range(30):
            g_func = random.choice(g_functions)
            g = g_func(n)
            
            norm = spectral_norm(g)
            a = [random.randint(0, 1) for _ in range(n)]
            discrepancy = vertex_star_discrepancy(g, a)
            
            results.append({
                "n": n,
                "g_function": g_func.__name__,
                "norm": norm,
                "discrepancy": discrepancy
            })
    
    min_lower_ratio = float('inf')
    max_upper_ratio = 0
    
    for result in results:
        lower_ratio = result["discrepancy"] / result["norm"]
        upper_ratio = result["discrepancy"] / (result["norm"] * math.log2(result["n"] + 1))
        
        if lower_ratio < min_lower_ratio:
            min_lower_ratio = lower_ratio
        if upper_ratio > max_upper_ratio:
            max_upper_ratio = upper_ratio
    
    return {
        "metric_name": "discrepancy_ratio",
        "metric_value": (min_lower_ratio, max_upper_ratio),
        "instances_tested": len(results),
        "conjecture_holds": min_lower_ratio >= 0.125 and max_upper_ratio <= 8 * math.log2(n + 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")