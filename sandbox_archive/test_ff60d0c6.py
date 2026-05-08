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

def random_triangle_free_graph(n):
    while True:
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    A[i][j] = A[j][i] = 1
        degree = [sum(row) for row in A]
        if all(d == 3 for d in degree) and not any(A[i][j] * A[j][k] * A[k][i] for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n)):
            return A

def max_cut(G):
    n = len(G)
    best_cut_value = -1
    for mask in range(1 << n):
        cut_value = sum(G[i][j] if (mask & (1 << i)) and not (mask & (1 << j)) else 0 for i in range(n) for j in range(i + 1, n))
        best_cut_value = max(best_cut_value, cut_value)
    return best_cut_value

def sdp_2(G):
    n = len(G)
    A = sum(G[i][j] * (i + 1) * (j + 1) for i in range(n) for j in range(i + 1, n))
    lambda_min = min(eigenvalue(A) for _ in range(10))  # Approximate eigenvalue
    return n / 4 * abs(lambda_min)

def perm(G):
    n = len(G)
    if n == 0:
        return 1
    result = 0
    for i in range(n):
        sign = (-1) ** (n - sum(row[i] for row in G))
        submatrix = [row[:i] + row[i+1:] for row in G[:i] + G[i+1:]]
        result += sign * perm(submatrix)
    return abs(result)

def eigenvalue(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * eigenvalue(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16, 18]
    results = []
    
    for n in n_values:
        for _ in range(30):
            G = random_triangle_free_graph(n)
            pi_G = (n / 3) * math.log2(6) - math.log2(perm(G))
            gap_G = max_cut(G) - sdp_2(G)
            results.append((pi_G, gap_G, n))
    
    pi_sqrt_n = [pi * math.sqrt(n) for pi, _, n in results]
    gap = [gap for _, gap, _ in results]
    
    rho = sum(pi * gap for pi, gap in zip(pi_sqrt_n, gap)) / (sum(pi ** 2 for pi in pi_sqrt_n) * sum(gap ** 2 for gap in gap))
    support_fraction = sum(1 for pi, gap in zip(pi_sqrt_n, gap) if gap >= pi * math.sqrt(n) / 100) / len(pi_sqrt_n)
    
    conjecture_holds = rho >= 0.5 and support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "gap",
        "metric_value": sum(gap) / len(gap),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds]
    support_fraction = sum(run_trial(seed)["conjecture_holds"] for seed in seeds) / len(seeds)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results):.6f} std={math.sqrt(sum((x - sum(results)/len(results))**2 for x in results)/len(results)):.6f} support_fraction={support_fraction:.6f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")