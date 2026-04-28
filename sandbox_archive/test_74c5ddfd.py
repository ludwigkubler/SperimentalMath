# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import combinations

# Helper functions for linear algebra
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return C

def gaussian_elimination(A, b):
    m = len(A)
    n = len(b)
    augmented = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(m):
        # Find the pivot
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Eliminate non-pivot elements
        for j in range(i+1, m):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    
    # Back-substitute to find the solution
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = augmented[i][n] / augmented[i][i]
        for j in range(i-1, -1, -1):
            augmented[j][n] -= augmented[j][i] * x[i]
    
    return x

# Helper functions for the conjecture
def walsh_coefficient(f, x):
    n = len(x)
    result = 0
    for i in range(2**n):
        sign = (-1) ** sum((x[j] & (1 << k)) != 0 for j in range(n))
        result += sign * f(i)
    return result / 2**n

def symmetric_difference_dimension(A, B):
    diff = A ^ B
    count = 0
    while diff:
        if diff & 1:
            count += 1
        diff >>= 1
    return count

def generate_NW_design(d, l, a, m):
    S = []
    for i in range(m):
        S.append(random.sample(range(2**d), random.randint(1, d)))
    return S

def compute_W(D):
    m = len(D)
    P_D = [[] for _ in range(1 << m)]
    
    # Generate the poset
    for T in range(1 << m):
        if T == 0:
            continue
        for i in range(m):
            if (T & (1 << i)) != 0:
                parent = T ^ (1 << i)
                P_D[parent].append(T)
    
    # Compute the antichain width
    W_D = 0
    for A in combinations(range(1 << m), len(A)):
        A_set = set(A)
        if all(symmetric_difference_dimension(T, U) % 2 == 1 for T in A_set for U in A_set if T != U):
            W_D = max(W_D, sum(2**(-len(S[i] for i in T)) for T in A))
    
    return W_D

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = random.randint(1, 20)
    l = random.choice([3, 4, 5])
    a = random.choice([2, 3])
    m = random.randint(4, 16)
    
    S = generate_NW_design(d, l, a, m)
    P_D = [[] for _ in range(1 << m)]
    
    # Generate the poset
    for T in range(1 << m):
        if T == 0:
            continue
        for i in range(m):
            if (T & (1 << i)) != 0:
                parent = T ^ (1 << i)
                P_D[parent].append(T)
    
    # Compute the antichain width
    W_D = max(sum(2**(-len(S[i] for i in T)) for T in A) for A in combinations(range(1 << m), len(A)))
    
    # Sample a hard function f as a random parity-balanced function
    x = [random.choice([0, 1]) for _ in range(d)]
    def f(i):
        return sum(x[j] & (1 << k) != 0 for j in range(d)) % 2
    
    eps = max(abs(walsh_coefficient(f, x)) for x in combinations(range(2**d), a))
    
    # Compute the maximum linear bias of NW_{D,f}
    max_bias = 0
    for T in range(1 << m):
        if T != 0:
            bias = abs(sum(f(i) for i in S[j] for j in range(m) if (T & (1 << j)) != 0))
            max_bias = max(max_bias, bias)
    
    # Check the conjecture
    conjecture_holds = max_bias <= W_D * eps
    
    return {
        "metric_name": "bias",
        "metric_value": max_bias,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_bias={max_bias} > W(D)*eps={W_D*eps}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_bias = sum(r["metric_value"] for r in results) / len(results)
    std_bias = math.sqrt(sum((r["metric_value"] - mean_bias)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_bias} std={std_bias} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_bias > W(D)*eps\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")