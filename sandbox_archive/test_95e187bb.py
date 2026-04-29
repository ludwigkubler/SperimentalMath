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

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i] = 0
                for k in range(i+1, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def or_function(x):
        return any(xi == 1 for xi in x)

    def equality_gadget(k):
        n = k * (k - 1)
        G = [[0] * n for _ in range(n)]
        for i in range(k):
            for j in range(i+1, k):
                idx1 = i * (k - 1) + j - 1
                idx2 = j * (k - 1) + i - 1
                G[idx1][idx2] = G[idx2][idx1] = 1
        return G

    def protocol_pullback(G, protocol):
        n = len(G)
        m = len(protocol)
        pullback = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if G[i][j]:
                    pullback[i][j] = protocol[(i // (k-1)) % m][(j // (k-1)) % m]
        return pullback

    def cover_multiplicity(pullback, R):
        n = len(pullback)
        max_multiplicity = 0
        for i in range(n):
            multiplicity = sum(1 for j in range(n) if pullback[i][j])
            if multiplicity > max_multiplicity:
                max_multiplicity = multiplicity
        return max_multiplicity

    def clc(f, G):
        n = len(G)
        k = int(math.sqrt(n))
        protocols = []
        for c in range(1, 20):  # Limiting cost to avoid excessive computation
            protocol = [random.choice([0, 1]) for _ in range(c)]
            if f(protocol):
                protocols.append((c, protocol))
        return protocols

    k_values = [5, 10, 15, 20, 30, 40]
    results = []
    for k in k_values:
        G = equality_gadget(k)
        n = len(G)
        f = or_function
        Q_f = n
        protocols = clc(f, G)
        if not protocols:
            return {
                "metric_name": "cover_multiplicity",
                "metric_value": 0,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "no_protocols_found"
            }
        max_multiplicity = 0
        for c, protocol in protocols:
            pullback = protocol_pullback(G, protocol)
            multiplicity = cover_multiplicity(pullback, n)
            if multiplicity > max_multiplicity:
                max_multiplicity = multiplicity
        results.append(max_multiplicity)

    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x >= 2**(Q_f * math.log2(k_values[-1] + 1))) / len(results)

    return {
        "metric_name": "cover_multiplicity",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_metric_value} std={std_metric_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean={mean_metric_value} std={std_metric_value}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no_protocols_found")