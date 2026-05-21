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
    
    n = 40
    d = 0.878 * math.log(n)
    if d < 3.5 * math.log(n):
        return {
            "metric_name": "rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "d is less than 3.5 log n"
        }
    
    # Generate a random Max-CUT instance
    vertices = list(range(n))
    edges = set()
    for _ in range(int(0.2 * n * (n - 1) / 2)):
        u, v = random.sample(vertices, 2)
        if u < v:
            edges.add((u, v))
    
    # Construct the degree-d pseudoexpectation moment matrix M
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        M[i][i] = n - 2 * sum(1 for u, v in edges if u == i)
        for j in range(i + 1, n):
            if (i, j) in edges or (j, i) in edges:
                M[i][j] = M[j][i] = 1
    
    # Compute the real rank of M via QR decomposition
    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q, R = [], []
        for k in range(n):
            u = [A[i][k] for i in range(k, m)]
            norm_u = sum(x * x for x in u) ** 0.5
            q = [x / norm_u if i == k else 0 for i, x in enumerate(u)]
            Q.append(q)
            r = [sum(A[i][j] * q[j] for j in range(k, n)) for i in range(k, m)]
            R.append(r)
        return Q, R
    
    Q, R = qr_decomposition(M)
    rank = sum(1 for row in R if any(x != 0 for x in row))
    
    # Check the conjecture
    if rank >= 3.5 * math.log(n):
        return {
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank < 3.5 log n (rank={rank}, d={d})"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results if "metric_value" in res)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if "metric_value" in res) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"])
    
    if support_fraction >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction / len(results):.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < 3.5 log n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")