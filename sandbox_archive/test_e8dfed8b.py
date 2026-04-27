# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def binomial_coefficient(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose_matrix(A):
    m = len(A)
    n = len(A[0])
    T = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            T[j][i] = A[i][j]
    return T

def permanent(B):
    n = len(B)
    if n == 1:
        return B[0][0]
    p = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in B[1:]]
        sign = (-1) ** j
        p += sign * B[0][j] * permanent(submatrix)
    return p

def sensitive_boundary_matrix(f, k=4):
    n = 2 ** (k - 1)
    B = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(x + 1, n):
            if sum(int(a) != int(b) for a, b in zip(bin(f"{x:0{k-1}b}"), bin(f"{y:0{k-1}b}"))) == 1 and f[x] != f[y]:
                B[x][y] = 1
    return B

def Q_dt(f):
    memo = {}
    
    def helper(subset):
        if not subset:
            return 0
        if tuple(sorted(subset)) in memo:
            return memo[tuple(sorted(subset))]
        
        min_val = float('inf')
        for i in range(len(subset)):
            new_subset = subset[:i] + subset[i+1:]
            max_val = -float('inf')
            for j in range(2):
                if j not in new_subset:
                    new_subset_with_j = new_subset + (j,)
                    max_val = max(max_val, helper(new_subset_with_j))
            min_val = min(min_val, max_val)
        
        memo[tuple(sorted(subset))] = min_val
        return min_val
    
    return helper(tuple(range(2**(k-1))))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k = 4
    num_functions = 2 ** (k * k)
    total_slack = 0
    worst_case_slack = float('-inf')
    instances_tested = 0
    
    for _ in range(num_functions):
        f = {bin(i)[2:].zfill(k): random.choice([0, 1]) for i in range(2**k)}
        
        B = sensitive_boundary_matrix(f)
        perm_B = permanent(B)
        Q_dt_f = Q_dt(f)
        
        slack = 4 * Q_dt_f - (perm_B + 1).bit_length()
        total_slack += slack
        worst_case_slack = max(worst_case_slack, slack)
        instances_tested += 1
    
    mean_slack = total_slack / instances_tested
    support_fraction = 0.0 if worst_case_slack < 0 else 1.0
    
    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if worst_case_slack >= 0 else f"worst_case_slack={worst_case_slack}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")