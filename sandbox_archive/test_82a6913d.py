# auto-injected by SEC sandbox
import collections
import json
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
from itertools import combinations

def generate_disjointness_matrix(n: int) -> list:
    M = [[0] * (2*n) for _ in range(n)]
    for i, j in combinations(range(n), 2):
        M[i][j + n] = 1
        M[j][i + n] = 1
    return M

def tensor_decomposition(M: list, n: int) -> int:
    rank = 0
    while True:
        found = False
        for i in range(n):
            for j in range(n):
                if M[i][j + n] != 0 and M[j][i + n] != 0:
                    A = [[M[k][l] - M[k][j + n] * M[l][i + n] for l in range(n)] for k in range(n)]
                    B = [[M[k][l] - M[k][i + n] * M[l][j + n] for l in range(n)] for k in range(n)]
                    rank += 1
                    found = True
        if not found:
            break
    return rank

def noncommutative_rank(M: list, n: int) -> float:
    x = [[0] * n for _ in range(n)]
    y = [[0] * n for _ in range(n)]
    for i in range(n):
        x[i][i] = 1
        y[i][i] = 1
    A = M
    tau_M_n = 0
    while A != [[0] * (2*n) for _ in range(n)]:
        tau_M_n += 1
        for i in range(n):
            for j in range(n):
                if A[i][j + n] != 0 and A[j][i + n] != 0:
                    x = [[A[k][l] - A[k][j + n] * A[l][i + n] for l in range(n)] for k in range(n)]
                    y = [[A[k][l] - A[k][i + n] * A[l][j + n] for l in range(n)] for k in range(n)]
                    break
            else:
                continue
            break
        A = [[x[i][j] - y[j] * M[i][n + j] for j in range(n)] for i in range(n)]
    return tau_M_n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    for n in n_values:
        M_n = generate_disjointness_matrix(n)
        tau_M_n = noncommutative_rank(M_n, n)
        if tau_M_n < 0.1 * n:
            return {
                "metric_name": "noncommutative_rank",
                "metric_value": tau_M_n,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, tau(M_n)={tau_M_n} < 0.1*n"
            }
        results.append(tau_M_n)
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "noncommutative_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": all(x >= 0.1 * n for n, x in zip(n_values, results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["conjecture_holds"]]
    support_fraction = len(results) / len(seeds)
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    print(f"{RESULT} mean={sum(results)/len(results):.2f} std={math.sqrt(sum((x - sum(results)/len(results))**2 for x in results) / len(results)):.2f} support_fraction={support_fraction:.2f}")