# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = 1 / A[i][i]
        for j in range(n):
            A[i][j] *= factor
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def symmetric_difference_dimension(S1, S2):
    diff = [x for x in S1 if x not in S2] + [x for x in S2 if x not in S1]
    return len(diff)

def walsh_coefficient(f, T):
    n = len(T)
    sum_val = 0
    for i in range(1 << n):
        prod = 1
        for j in range(n):
            if (i >> j) & 1:
                prod *= f[T[j]]
        sum_val += prod
    return sum_val / (1 << n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d, l, a, m = random.choice([(5, 3, 2, 4), (8, 4, 2, 8), (11, 5, 2, 16), (14, 3, 3, 4), (14, 4, 3, 8)])
    S = [set(random.sample(range(d), random.randint(1, d))) for _ in range(m)]
    
    P_D = []
    for i in range(1 << m):
        subset = {j for j in range(m) if (i >> j) & 1}
        if all(symmetric_difference_dimension(subset, T) % 2 == 0 for T in P_D):
            P_D.append(subset)
    
    W_D = max(sum(2**(-len(S[i] for i in T)) for T in A) for A in P_D)
    
    f = [random.choice([-1, 1]) for _ in range(d)]
    eps = max(walsh_coefficient(f, S_i) for S_i in S if len(S_i) <= a)
    bias = max(abs(sum(f[i] for i in T)) for T in P_D)
    
    return {
        "metric_name": "bias",
        "metric_value": bias,
        "instances_tested": 1,
        "conjecture_holds": bias <= 1.05 * W_D * eps,
        "counterexample": "" if bias <= 1.05 * W_D * eps else f"bias={bias} > 1.05 * {W_D}*{eps}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_bias = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_bias)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_bias} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")