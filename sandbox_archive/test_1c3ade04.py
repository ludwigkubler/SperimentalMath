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
    
    def f(x, y):
        return x == y
    
    M = communication_matrix(f)
    n = len(M)
    P_f = maximal_rectangles(M)
    mu_f = moebius_function(P_f)
    MM_f = total_moebius_mass(mu_f, P_f)
    D_cc_f = disjointness_communication_complexity(f)
    
    return {
        "metric_name": "log2_MM",
        "metric_value": math.log2(MM_f),
        "instances_tested": 1,
        "conjecture_holds": log2_MM >= D_cc_f / 4 if D_cc_f >= 4 else False,
        "counterexample": "" if (D_cc_f < 4 or log2_MM >= D_cc_f / 4) else f"Counterexample: D^cc(f)={D_cc_f}, log2 MM(f)={log2_MM}"
    }

def communication_matrix(func):
    n = len(next(iter(func.values())))
    M = [[func((i, j), (x, y)) for x in range(n)] for i in range(n)]
    return M

def maximal_rectangles(M):
    def support(row):
        return [j for j, val in enumerate(row) if val == 1]
    
    P_f = []
    n = len(M)
    for A in range(1 << n):
        rows_A = [i for i in range(n) if (A & (1 << i)) != 0]
        B = set.intersection(*[set(support(M[i])) for i in rows_A])
        if B and all((A & (1 << i)) != 0 for i in rows_A):
            P_f.append((rows_A, list(B)))
    return P_f

def moebius_function(P_f):
    n = len(P_f)
    mu = [[0] * n for _ in range(n)]
    
    def dfs(i, j):
        if i == j:
            return 1
        if i > j:
            return 0
        mu[i][j] = -sum(mu[i][k] for k in range(i+1, j))
        return mu[i][j]
    
    for i in range(n):
        dfs(0, i)
    return mu

def total_moebius_mass(mu_f, P_f):
    MM_f = sum(abs(mu_f[i][j]) for i in range(len(P_f)) for j in range(i+1, len(P_f)))
    return MM_f

def disjointness_communication_complexity(func):
    n = len(next(iter(func.values())))
    def partition_number(submat):
        if not submat:
            return 0
        m = len(submat)
        dp = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(i, m + 1):
                dp[i][j] = dp[i-1][j] + sum(func((i-1, k), (x, y)) for x in range(n) for y in range(n))
        return dp[1][m]
    
    memo = {}
    def memoized_partition_number(submat):
        if not submat:
            return 0
        key = tuple(tuple(row) for row in submat)
        if key not in memo:
            memo[key] = partition_number(submat)
        return memo[key]
    
    def submatrix(A, B):
        return [[func((i, j), (x, y)) for x in A for y in B] for i in range(n) for j in range(n)]
    
    def all_subsets(s):
        subsets = []
        for r in range(1 << len(s)):
            subset = [s[i] for i in range(len(s)) if (r & (1 << i)) != 0]
            subsets.append(subset)
        return subsets
    
    max_partition_size = 0
    for A in all_subsets(range(n)):
        for B in all_subsets(range(n)):
            submat = submatrix(A, B)
            partition_size = memoized_partition_number(submat)
            if partition_size > max_partition_size:
                max_partition_size = partition_size
    
    return max_partition_size

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_log2_MM = sum(r["metric_value"] for r in results) / len(results)
    std_log2_MM = math.sqrt(sum((r["metric_value"] - mean_log2_MM)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log2_MM} std={std_log2_MM} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")