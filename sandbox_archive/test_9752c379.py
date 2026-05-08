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

def lanczos(A, v0, k):
    n = len(A)
    v = [v0]
    H = []
    for _ in range(k):
        w = A @ v[-1]
        alpha = sum(v[-1][i] * w[i] for i in range(n))
        w -= alpha * v[-1]
        beta = math.sqrt(sum(w[i] ** 2 for i in range(n)))
        if beta == 0:
            break
        v.append(w / beta)
        H.append([alpha, beta])
    return v, H

def chebyshev_recurrence(A, b, k):
    n = len(A)
    sigma = [[0] * (k + 2) for _ in range(k + 1)]
    sigma[0][0] = 1
    sigma[1][1] = 1
    for i in range(2, k + 1):
        sigma[i][i] = 1
        for j in range(i - 1, -1, -1):
            sigma[j][i] = (A @ sigma[j][i - 1]) / b[i]
            sigma[j][i - 1] -= A @ sigma[j + 1][i - 1]
    return sigma

def max_cut(G):
    n = len(G)
    best_cut = 0
    for i in range(1 << n):
        cut_size = sum((i >> j) & 1 for j in range(n))
        if cut_size > n // 2:
            continue
        cut_value = sum(G[i][j] * ((i >> j) & 1) * ((i >> k) & 1) for j in range(n) for k in range(j + 1, n))
        best_cut = max(best_cut, cut_value)
    return best_cut

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 14, 18, 20])
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
        for j in range(i + 1, n):
            if random.random() < 3 / (2 * n - 4):
                G[i][j] = G[j][i] = 1
    
    v0 = [random.random() for _ in range(n)]
    v, H = lanczos(G, v0, 12)
    moments = [sum(v[-1][i] ** j for i in range(n)) / n for j in range(13)]
    
    sigma = chebyshev_recurrence(G, [math.sqrt(moments[i]) for i in range(1, 6)], 5)
    a = [sigma[0][i] - sigma[1][i] * sigma[2][i] / sigma[1][1] for i in range(3)]
    b = [math.sqrt(sigma[i + 1][i + 1] / sigma[i][i]) for i in range(5)]
    
    max_cut_value = max_cut(G)
    rho_G = max_cut_value / ((n / 4) * (3 - moments[2]))
    J_G = b[2] - math.sqrt(2)
    
    conjecture_holds = True
    counterexample = ""
    if rho_G >= 0.879 and J_G < -4 * math.log(n) / math.sqrt(n):
        conjecture_holds = False
        counterexample = f"ρ(G)={rho_G}, J(G)={J_G}, n={n}"
    
    return {
        "metric_name": "Jacobi Defect",
        "metric_value": J_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_J = sum(r["metric_value"] for r in results) / len(results)
    std_J = math.sqrt(sum((r["metric_value"] - mean_J) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_J} std={std_J} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE not enough seeds tested or no clear outcome")