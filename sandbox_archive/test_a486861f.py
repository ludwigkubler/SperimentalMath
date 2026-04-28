# auto-injected by SEC sandbox
import math
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

import json
import random

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
    return num // denom

def power_of_two(x):
    return x and not (x & (x - 1))

def compute_M_k(f, k):
    M_k = set()
    for minterm in f:
        if sum(minterm) == k:
            M_k.add(tuple(sorted(minterm)))
    return M_k

def compute_partial(M_k):
    partial = set()
    for minterm in M_k:
        for i in range(len(minterm)):
            new_minterm = list(minterm)
            new_minterm[i] = 0
            partial.add(tuple(sorted(new_minterm)))
    return partial

def compute_KK_lower(m, k):
    if k == 1:
        return m
    if k == m:
        return 1
    return sum(binomial(m - i, k - 1) for i in range(k))

def compute_D_m(f, M_k):
    n = len(next(iter(M_k)))
    R = set()
    T = set(range(n))
    memo = {}

    def D_m_helper(R, T):
        if (R, T) in memo:
            return memo[(R, T)]
        if not R:
            return 0
        if any(x[i] == 1 and y[i] == 0 for x, y in R):
            return 0
        min_val = float('inf')
        for i in range(n):
            R_0 = {(x, y) for x, y in R if x[i] == 0}
            R_1 = {(x, y) for x, y in R if x[i] == 1}
            min_val = min(min_val, 1 + max(D_m_helper(R_0, T), D_m_helper(R_1, T)))
        memo[(R, T)] = min_val
        return min_val

    return D_m_helper(R, T)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5]
    if seed == 0:
        n_values.extend([6, 7])
    results = []

    for n in n_values:
        if n == 4 or n == 5:
            # Enumerate all monotone Boolean functions on n
            from itertools import combinations
            M = list(combinations(range(n), n))
            f = [tuple(sorted(m)) for m in M]
        else:
            # Sample random monotone clutters on n
            f = []
            for _ in range(2000):
                k = random.randint(1, n)
                antichain = set(combinations(range(n), k))
                upper_closure = set()
                for x in antichain:
                    for y in M:
                        if all(xi <= yi for xi, yi in zip(x, y)):
                            upper_closure.add(tuple(sorted(y)))
                f.append(upper_closure)

        for f_instance in f:
            M_k = {compute_M_k(f_instance, k) for k in range(n + 1)}
            partial = compute_partial(M_k)
            Delta_KK = max(len(partial) - compute_KK_lower(len(minterms), k) for k, minterms in enumerate(M_k))
            D_m = compute_D_m(f_instance, M_k)

            results.append({
                "n": n,
                "Delta_KK": Delta_KK,
                "D_m": D_m
            })

    if not results:
        return {
            "metric_name": "D_m vs Delta_KK",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    metric_values = [result["Delta_KK"] for result in results]
    D_m_values = [result["D_m"] for result in results]

    from scipy.stats import spearmanr
    rho, _ = spearmanr(metric_values, D_m_values)

    tightness_ratio = [max(0, (D_m - 1) / (log2(Delta_KK + 2))) for Delta_KK, D_m in zip(metric_values, D_m_values)]
    tightness_histogram = {i: tightness_ratio.count(i) for i in set(tightness_ratio)}

    return {
        "metric_name": "D_m vs Delta_KK",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": all(D_m >= ceil(log2(Delta_KK + 2)) for Delta_KK, D_m in zip(metric_values, D_m_values)),
        "counterexample": "" if all(D_m >= ceil(log2(Delta_KK + 2)) for Delta_KK, D_m in zip(metric_values, D_m_values)) else "minimum-D_m violator"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = (sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")