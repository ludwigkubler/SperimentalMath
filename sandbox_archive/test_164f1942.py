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
    n = 40
    max_instances = 30
    instances_tested = min(max_instances, 2 * n)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def random_read_twice_bp(n, instances_tested):
        BPs = []
        for _ in range(instances_tested):
            bp = [[random.choice([-1, 1]) for _ in range(2)] for _ in range(n)]
            BPs.append(bp)
        return BPs

    def path_distribution(bp):
        m = len(bp)
        dp = [0] * (1 << m)
        dp[0] = 1
        for i in range(m):
            new_dp = [0] * (1 << m)
            for j in range(1 << m):
                if dp[j] > 0:
                    new_dp[j ^ bp[i][0]] += dp[j]
                    new_dp[j ^ bp[i][1]] += dp[j]
            dp = new_dp
        return dp

    def moments(dp, order):
        moments = [0] * (order + 1)
        for i in range(1 << len(dp)):
            weight = dp[i]
            moment = sum((i & (1 << j)) != 0 for j in range(len(dp))) ** 2
            for k in range(order):
                moments[k] += weight * moment ** (k // 2)
        return moments

    def free_cumulants(moments):
        cumulants = [moments[0]]
        for i in range(1, len(moments)):
            cumulant = moments[i]
            for j in range(i):
                cumulant -= sum(cumulants[j] * comb(i, j) * (i - j) ** (i - 2 * j) for j in range(j + 1))
            cumulants.append(cumulant)
        return cumulants

    def IP_2_path_distribution(n):
        A = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        dp = [0] * (1 << n)
        dp[0] = 1
        for i in range(n):
            new_dp = [0] * (1 << n)
            for j in range(1 << n):
                if dp[j] > 0:
                    new_dp[j ^ A[i][j & (n - 1)]] += dp[j]
            dp = new_dp
        return dp

    def IP_2_moments(dp, order):
        moments = [0] * (order + 1)
        for i in range(1 << len(dp)):
            weight = dp[i]
            moment = sum((i & (1 << j)) != 0 for j in range(len(dp))) ** 2
            for k in range(order):
                moments[k] += weight * moment ** (k // 2)
        return moments

    def IP_2_free_cumulants(moments):
        cumulants = [moments[0]]
        for i in range(1, len(moments)):
            cumulant = moments[i]
            for j in range(i):
                cumulant -= sum(cumulants[j] * comb(i, j) * (i - j) ** (i - 2 * j) for j in range(j + 1))
            cumulants.append(cumulant)
        return cumulants

    BPs = random_read_twice_bp(n, instances_tested)
    IP_2_dp = IP_2_path_distribution(n)
    IP_2_moments = IP_2_moments(IP_2_dp, 40)
    IP_2_cumulants = IP_2_free_cumulants(IP_2_moments)

    max_rho = 5 * math.log(n)
    rho_holds = True
    counterexample = ""

    for bp in BPs:
        dp = path_distribution(bp)
        moments = moments(dp, 40)
        cumulants = free_cumulants(moments)
        if abs(cumulants[-1]) > max_rho:
            rho_holds = False
            counterexample = "BP with high rho found"
            break

    return {
        "metric_name": "rho",
        "metric_value": abs(IP_2_cumulants[-1]),
        "instances_tested": instances_tested,
        "conjecture_holds": rho_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")