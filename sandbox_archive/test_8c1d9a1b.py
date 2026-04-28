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

def run_trial(seed: int) -> dict:
    def min_certificates(f):
        n = len(f)
        certificates = []
        for i in range(2**n):
            cert = [i >> j & 1 for j in range(n)]
            if all(f[tuple(cert)] == f[tuple(c ^ mask)] for t, c in enumerate(certificates)):
                continue
            certificates.append(cert)
        return certificates

    def conflict_graph(certificates):
        n = len(certificates[0])
        graph = [[0] * len(certificates) for _ in range(len(certificates))]
        for i, C in enumerate(certificates):
            for j, C_prime in enumerate(certificates):
                if any(C[v] != C_prime[v] for v in range(n)):
                    graph[i][j] = 1
        return graph

    def laplacian_matrix(graph):
        n = len(graph)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(graph[i])
            L[i][i] = -degree
            for j in range(i + 1, n):
                if graph[i][j]:
                    L[i][j] = L[j][i] = 1
        return L

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            minor = [[matrix[i][k] for k in range(j, n - 1)] for i in range(1, n)]
            det += ((-1) ** j) * matrix[0][j] * determinant(minor)
        return det

    def minmax_dp(f, mask):
        @lru_cache(None)
        def dp(i, mask):
            if i == len(f):
                return 0
            max_val = -math.inf
            for val in [0, 1]:
                new_mask = mask | (val << i)
                if all(f[tuple(new_mask)] == f[tuple(new_mask ^ (1 << j))] for j in range(i + 1)):
                    continue
                max_val = max(max_val, dp(i + 1, new_mask))
            return max_val
        return dp(0, mask)

    def Q_dt(f):
        n = len(f)
        k = sum(f.values())
        dp_values = [minmax_dp(f, (1 << i)) for i in range(n)]
        dt = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[tuple(dp_values[i] ^ dp_values[j])] != f[tuple(dp_values[i] ^ dp_values[j] ^ (1 << j))]:
                    dt += 1
        return dt

    def log2(x):
        return math.log2(x)

    random.seed(seed)
    k = random.choice([3, 4, 5, 6])
    f = {tuple(random.randint(0, 1) for _ in range(k)): random.randint(0, 1) for _ in range(2**k)}
    certificates = min_certificates(f)
    graph = conflict_graph(certificates)
    L = laplacian_matrix(graph)
    tau_Gf = determinant(L)
    Q_dt_f = Q_dt(f)
    delta_f = log2(tau_Gf) - Q_dt_f * log2(k + 1)

    return {
        "metric_name": "Delta",
        "metric_value": delta_f,
        "instances_tested": 1,
        "conjecture_holds": delta_f <= 0,
        "counterexample": "" if delta_f <= 0 else "delta > 0"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_delta = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std=0.0 support_fraction=1.0")
    elif any(r["metric_value"] > 1e-9 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"delta > 0\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")