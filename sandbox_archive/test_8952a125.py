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

def binomial(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def choose(n, k):
    if k == 0 or k == n:
        return 1
    return binomial(n, k)

def random_antichain(n):
    antichain = set()
    for _ in range(2**n - 1):
        subset = [i for i in range(n) if random.choice([True, False])]
        if all(len(subset & s) == 0 for s in antichain):
            antichain.add(frozenset(subset))
    return antichain

def min_max_dp(X, Y):
    n, m = len(X), len(Y)
    dp = [[math.inf] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        dp[i][0] = max(dp[i - 1][0], X[i - 1])
    for j in range(1, m + 1):
        dp[0][j] = max(dp[0][j - 1], Y[j - 1])
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = min(max(dp[i - 1][j], X[i - 1]), max(dp[i][j - 1], Y[j - 1]))
    return dp[n][m]

def compute_pd(f, n):
    Δ_f = {frozenset(s) for s in range(2**n) if f(s) == 0}
    pd = 0
    for T in range(n + 1):
        Δ_f_T = {S for S in Δ_f if all(x in T for x in S)}
        boundary_matrix = []
        for k in range(len(Δ_f_T)):
            row = [0] * (len(Δ_f_T) - k)
            for i, s in enumerate(Δ_f_T):
                for j, t in enumerate(Δ_f_T):
                    if s.issubset(t):
                        row[j] += 1
            boundary_matrix.append(row)
        ker_dim = sum(1 for r in boundary_matrix if all(x == 0 for x in r))
        rank = len(boundary_matrix) - ker_dim
        pd = max(pd, T - ker_dim - 1)
    return pd

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4]
    if seed % 2 == 0:
        n_values.append(5)
    results = []
    for n in n_values:
        if n == 3 or n == 4:
            for _ in range(1):
                f = lambda s: any(x not in s for x in [0, 1, 2])
                D_m_f = min_max_dp([x for x in range(n)], [n - x - 1 for x in range(n)])
                Pd_f = compute_pd(f, n)
                results.append({"metric_name": "D_m(f)", "metric_value": D_m_f, "instances_tested": 1, "conjecture_holds": D_m_f >= Pd_f, "counterexample": ""})
        else:
            for _ in range(500):
                antichain = random_antichain(n)
                f = lambda s: any(x not in s for x in [0, 1, 2, 3, 4])
                D_m_f = min_max_dp([x for x in range(n)], [n - x - 1 for x in range(n)])
                Pd_f = compute_pd(f, n)
                results.append({"metric_name": "D_m(f)", "metric_value": D_m_f, "instances_tested": 1, "conjecture_holds": D_m_f >= Pd_f, "counterexample": ""})
    return {"seed": seed, "results": results}

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
        all_results.extend(result["results"])
    
    D_m_values = [r["metric_value"] for r in all_results if r["metric_name"] == "D_m(f)"]
    Pd_values = [r["metric_value"] for r in all_results if r["metric_name"] == "Pd(f)"]
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={sum(D_m_values)/len(D_m_values)} std={math.sqrt(sum((x - sum(D_m_values)/len(D_m_values))**2 for x in D_m_values) / len(D_m_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in enumerate(all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")