# auto-injected by SEC sandbox
import math
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
from collections import defaultdict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def binomial(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def kruskal_katona(m, k):
    return sum(binomial(m // (2 ** i), k) for i in range(k))

def powerset(s):
    result = []
    for subset_size in range(len(s) + 1):
        for subset in itertools.combinations(s, subset_size):
            result.append(set(subset))
    return result

def hamming_weight(x):
    return bin(x).count('1')

def is_monotone(f):
    n = len(f)
    for i in range(1 << n):
        if any(f[i | (1 << j)] < f[i] for j in range(n)):
            return False
    return True

def compute_M_k(f, k):
    n = len(f)
    M_k = set()
    for x in range(1 << n):
        if hamming_weight(x) == k:
            M_k.add(x)
    return M_k

def compute_partial(M_k):
    n = max(M_k).bit_length() - 1
    partial_M_k = set()
    for x in M_k:
        for y in range(1 << n):
            if (x & y) == 0 and (y | x) in M_k:
                partial_M_k.add(y)
    return partial_M_k

def compute_D_m(R, memo):
    if not R:
        return 0
    if R in memo:
        return memo[R]
    n = len(R[0])
    min_d = float('inf')
    for i in range(n):
        R_0 = {(x[:i] + '0' + x[i+1:], y) for x, y in R}
        R_1 = {(x[:i] + '1' + x[i+1:], y) for x, y in R}
        d_0 = compute_D_m(R_0, memo)
        d_1 = compute_D_m(R_1, memo)
        min_d = min(min_d, 1 + max(d_0, d_1))
    memo[R] = min_d
    return min_d

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6, 7]
    results = []
    
    for n in n_values:
        if n <= 5:
            # Enumerate all monotone Boolean functions on n
            from itertools import combinations
            elements = list(range(n))
            f_list = set()
            for subset in combinations(elements, n):
                f = [0] * (1 << n)
                for i in range(1 << n):
                    if binomial(i, hamming_weight(i)) % 2 == 1:
                        f[i] = 1
                f_list.add(tuple(f))
        else:
            # Sample random monotone clutters on n
            from itertools import combinations
            elements = list(range(n))
            f_list = set()
            for _ in range(2000):
                k = random.randint(1, n)
                antichain = set(combinations(elements, k))
                upper_closure = set()
                for x in powerset(elements):
                    if all(x <= y for y in antichain):
                        upper_closure.add(frozenset(x))
                f = [0] * (1 << n)
                for x in upper_closure:
                    f[frozenset(x)] = 1
                f_list.add(tuple(f))
        
        for f in f_list:
            M_k = {compute_M_k(f, k) for k in range(n + 1)}
            partial_M_k = {compute_partial(M_k[k]) for k in range(1, n + 1)}
            Delta_KK = max(len(partial_M_k) - kruskal_katona(len(M_k), k) for k in range(1, n + 1))
            D_m = compute_D_m((frozenset(), frozenset()), {})
            results.append({
                "n": n,
                "Delta_KK": Delta_KK,
                "D_m": D_m
            })
    
    metric_value = sum(result["D_m"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(result["D_m"] >= math.ceil(math.log2(result["Delta_KK"] + 2)) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "D_m",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")