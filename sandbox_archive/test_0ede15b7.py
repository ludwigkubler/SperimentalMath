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
    
    def partition_number(n):
        if n == 0:
            return 1
        p = [0] * (n + 1)
        p[0] = 1
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                p[j] += p[j - i]
        return p[n]

    def communication_complexity(M):
        n = len(M)
        dp = [[0] * (1 << n) for _ in range(n)]
        for mask in range(1 << n):
            dp[0][mask] = 1 if all(M[i][j] == M[i][k] for j, k in itertools.combinations(range(n), 2)) else 0
        for i in range(1, n):
            for mask in range(1 << n):
                dp[i][mask] = max(dp[i - 1][s] + dp[i - 1][mask ^ s] for s in range(1 << n) if (s & mask) == s)
        return dp[n - 1][(1 << n) - 1]

    def communication_matrix(f):
        n = len(f)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M[i][j] = f[i][j]
        return M

    def max_ones_rectangles(M):
        n = len(M)
        rectangles = []
        for A in range(1 << n):
            B = set()
            for x in range(n):
                if (A & (1 << x)) != 0:
                    B.update([j for j in range(n) if M[x][j] == 1])
            if len(B) == len(B.intersection(set(range(n)))):
                rectangles.append((set(bin(A)[2:].zfill(n)), B))
        return rectangles

    def poset_to_mobius_function(rectangles):
        n = len(rectangles)
        mu = [[0] * n for _ in range(n)]
        for i in range(n):
            mu[i][i] = 1
        for r in range(n - 2, -1, -1):
            for s in range(r + 1, n):
                if rectangles[r][0].issubset(rectangles[s][0]):
                    mu[r][s] = -sum(mu[r][t] for t in range(r + 1, s) if rectangles[t][0].issubset(rectangles[s][0]))
        return mu

    def mobius_mass(M):
        n = len(M)
        rectangles = max_ones_rectangles(M)
        poset = [(rectangles[i], rectangles[j]) for i in range(len(rectangles)) for j in range(i + 1, len(rectangles))]
        mu = poset_to_mobius_function(poset)
        return sum(abs(mu[i][j]) for i, j in poset)

    def f_disj(x, y):
        return any(xi != yi for xi, yi in zip(x, y))

    def f_eq(x, y):
        return all(xi == yi for xi, yi in zip(x, y))

    def f_gt(x, y):
        return any(xi > yi for xi, yi in zip(x, y))

    def f_ip(x, y):
        return all(xi * yi == 0 for xi, yi in zip(x, y))

    def f_andor(x, y):
        return any(xi != yi for xi, yi in zip(x, y)) or all(xi == yi for xi, yi in zip(x, y))

    functions = [f_disj, f_eq, f_gt, f_ip, f_andor]
    p_values = [0.25, 0.5]

    results = []
    for n in range(3, 9):
        for func in functions:
            M = communication_matrix(func)
            D_cc = communication_complexity(M)
            if D_cc >= 4:
                MM = mobius_mass(M)
                results.append({
                    "metric_name": "log2_MM",
                    "metric_value": math.log2(MM),
                    "instances_tested": 1,
                    "conjecture_holds": math.log2(MM) >= D_cc / 4,
                    "counterexample": ""
                })

        for p in p_values:
            f = [[random.choice([0, 1]) if random.random() < p else 0 for _ in range(n)] for _ in range(n)]
            M = communication_matrix(f)
            D_cc = communication_complexity(M)
            if D_cc >= 4:
                MM = mobius_mass(M)
                results.append({
                    "metric_name": "log2_MM",
                    "metric_value": math.log2(MM),
                    "instances_tested": 1,
                    "conjecture_holds": math.log2(MM) >= D_cc / 4,
                    "counterexample": ""
                })

    total_metric = sum(result["metric_value"] for result in results)
    num_supporting = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = num_supporting / len(results)

    return {
        "seed": seed,
        "mean_log2_MM": total_metric / len(results),
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric = sum(result["mean_log2_MM"] for result in results)
    num_supporting = sum(1 for result in results if result["support_fraction"] >= 0.8)
    support_fraction = num_supporting / len(results)

    if num_supporting == len(results):
        print(f"RESULT: SUPPORTED mean={total_metric/len(results):.4f} std=NA support_fraction={support_fraction:.2f}")
    elif any(result["support_fraction"] < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction<0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")