# auto-injected by SEC sandbox
import random
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def binomial(n, k):
    if k > n:
        return 0
    num = 1
    denom = 1
    for i in range(k):
        num *= (n - i)
        denom *= (i + 1)
    return Fraction(num, denom)

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        pivot_row = -1
        for i in range(rank, m):
            if matrix[i][j] != 0:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        rank += 1
        for i in range(m):
            if i != rank - 1:
                factor = matrix[i][j] / matrix[rank - 1][j]
                for k in range(n):
                    matrix[i][k] -= factor * matrix[rank - 1][k]
    return rank

def monomial_to_index(monomial, m):
    index = 0
    power = m
    for coeff in monomial:
        index += coeff * power
        power //= m
    return index

def generate_permutation_tensor(m):
    tensor = []
    for i in range(m**m):
        row = [0] * (m**m)
        row[i] = 1
        tensor.append(row)
    return tensor

def generate_det_n_tensor(n, m):
    if n < m**2:
        raise ValueError("n must be at least m^2")
    tensor = []
    for i in range(m**m):
        row = [0] * (m**m)
        row[i % m**2] = 1
        tensor.append(row)
    return tensor

def young_flattening_rank(tensor, m, k):
    n = len(tensor)
    syt_count = binomial(m, k) * lcm(k, m-k)
    M_k = [[0] * (m**m) for _ in range(syt_count)]
    
    # Generate Young flattening matrix
    row_index = 0
    for i in range(1, m+1):
        for j in range(i):
            if j + k > m:
                continue
            monomial = [0] * m
            monomial[j] = 1
            monomial[j+k] = 1
            index = monomial_to_index(monomial, m)
            M_k[row_index][index] = 1
            row_index += 1
    
    # Compute rank using Gaussian elimination
    return gaussian_elimination(M_k)

def run_trial(seed: int) -> dict:
    import random
    random.seed(seed)
    
    results = []
    for m in [2, 3, 4]:
        for n in range(m**2, m**2 + 5):
            Per_m = generate_permutation_tensor(m)
            det_n = generate_det_n_tensor(n, m)
            
            YF_k_Per_m = young_flattening_rank(Per_m, m, k)
            YF_k_det_n = young_flattening_rank(det_n, m, k)
            
            delta = YF_k_det_n - YF_k_Per_m
            C_m_k = binomial(m, k) * (n - m**2 + 1)
            conjecture_holds = delta >= 0.5 * C_m_k
            
            results.append({
                "m": m,
                "n": n,
                "YF_k_Per_m": YF_k_Per_m,
                "YF_k_det_n": YF_k_det_n,
                "delta": delta,
                "C_m_k": C_m_k,
                "conjecture_holds": conjecture_holds
            })
    
    metric_value = sum(result["delta"] for result in results) / len(results)
    max_YF_k_Per_m = max(result["YF_k_Per_m"] for result in results)
    brk = {2: 2, 3: 7}
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    counterexample = ""
    for result in results:
        if not result["conjecture_holds"]:
            counterexample = f"m={result['m']}, n={result['n']}, delta={result['delta']}"
            break
    
    return {
        "metric_name": "delta(m,k,n)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={first_failing_seed}")