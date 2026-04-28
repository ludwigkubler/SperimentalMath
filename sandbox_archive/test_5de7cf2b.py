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

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

def d_pluss(x, y):
    return sum(hamming_distance(xi, yi) for xi, yi in zip(x, y))

def sdp_solve(L):
    n = len(L)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = (L[i][i] + L[j][j] - L[i][j]) / 2
            D[j][i] = D[i][j]
    
    # Cholesky decomposition
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                sum_k = sum(A[k][k] ** 2 for k in range(j))
                A[j][j] = math.sqrt(L[j][j] - sum_k)
            else:
                sum_k = sum(A[k][j] * A[k][i] for k in range(j))
                A[j][i] = (L[j][i] - sum_k) / A[i][i]
    
    return A

def property_a_expand(X, Y, F):
    n = len(X)
    d_pluss = lambda x, y: sum(hamming_distance(xi, yi) for xi, yi in zip(x, y))
    L = [[d_pluss(X[i], X[j]) for j in range(len(X))] for i in range(len(X))]
    A = sdp_solve(L)
    
    φ = {}
    for x in X:
        φ[x] = [A[i][X.index(x)] for i in range(n)]
    
    return φ

def coarse_pullback_protocol(φ, G):
    n = len(G)
    m_Π = 1
    for g in G:
        m_Π *= sum(1 for x in G if all(abs(φ[x][i] - φ[g[i]][i]) < 1e-6 for i in range(n)))
    return m_Π

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    gadgets = {
        "IND_2": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "EQ_2": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "IP_2": [[0, 0], [0, 1], [1, 0], [1, 1]]
    }
    
    predicates = {
        "AND_n": lambda x: all(xi == 1 for xi in x),
        "OR_n": lambda x: any(xi == 1 for xi in x),
        "PARITY_n": lambda x: sum(xi for xi in x) % 2 == 0
    }
    
    results = []
    for gadget_name, G in gadgets.items():
        n_values = [2, 3, 4]
        for n in n_values:
            X = list(combinations(range(n), n // 2))
            Y = list(combinations(range(n), n // 2))
            F = [set() for _ in range(3)]
            F[0] = {tuple(sorted(x)) for x in X}
            F[1] = {tuple(sorted(x + y)) for x, y in combinations(X, 2)}
            F[2] = {tuple(sorted(x + y + z)) for x, y, z in combinations(X, 3)}
            
            φ = property_a_expand(X, Y, F)
            α = sum(math.log(abs(φ[x][i] - φ[y][i])) / math.log(len(G)) for x, y in combinations(X, 2) for i in range(n)) / (n * len(X))
            
            f_name = random.choice(list(predicates.keys()))
            f = predicates[f_name]
            Q_f = n
            
            min_cost = float('inf')
            for c in range(math.ceil(α * Q_f)):
                protocol = []
                for _ in range(c):
                    protocol.append(random.choice([0, 1]))
                if all(f(tuple(sorted(x + y)) == protocol) for x, y in combinations(X, 2)):
                    min_cost = c
                    break
            
            m_Π = coarse_pullback_protocol(φ, G)
            
            results.append({
                "metric_name": "slack",
                "metric_value": min_cost - α * Q_f,
                "instances_tested": 1,
                "conjecture_holds": min_cost >= math.floor(α * Q_f) and m_Π >= 2 ** (α * Q_f) / 2,
                "counterexample": ""
            })
    
    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_slack) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_slack": mean_slack,
        "std_dev": std_dev,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(r["mean_slack"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["mean_slack"] - mean_slack) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slack} std={std_dev} support_fraction={support_fraction}")
    elif any(r["support_fraction"] < 0.8 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient trials")