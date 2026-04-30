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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        for j in range(i+1, n):
            factor = Augmented[j][i] / Augmented[i][i]
            for k in range(n + 1):
                Augmented[j][k] -= factor * Augmented[i][k]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = Augmented[i][n] / Augmented[i][i]
        for j in range(i-1, -1, -1):
            Augmented[j][n] -= Augmented[j][i] * x[i]
    return x

def vc_dimension(S, max_size=6):
    n = len(S)
    for d in range(1, max_size + 1):
        if all(any(all(s[i] == t[i] for i in range(d)) for s in S) for t in S):
            return d
    return max_size

def generate_k_clique_dnf(n, k):
    terms = []
    for subset in itertools.combinations(range(n), k):
        term = [0] * n
        for node in subset:
            term[node] = 1
        terms.append(term)
    return terms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 15, 20]
    results = []
    
    for n in n_values:
        k_clique_dnf = generate_k_clique_dnf(n, 3)
        S_F = set(tuple(term) for term in k_clique_dnf)
        
        v = vc_dimension(S_F)
        if v < 6:
            return {
                "metric_name": "VC-dimension",
                "metric_value": v,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": "VC-dimension too small"
            }
        
        F_size = len(k_clique_dnf)
        if F_size < 2**(v/4):
            return {
                "metric_name": "DNF size",
                "metric_value": F_size,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"DNF size {F_size} < 2^{v/4}"
            }
        
        results.append(F_size)
    
    return {
        "metric_name": "DNF size",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='VC-dimension too small' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient evidence")