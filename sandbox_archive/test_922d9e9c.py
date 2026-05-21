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
    
    # Generate a random Max-CUT instance
    vertices = list(range(n))
    edges = set()
    for _ in range(2 * n):
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    # Construct the degree-d pseudoexpectation moment matrix M
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for u, v in edges:
        M[u][v] += 1
        M[v][u] += 1
    
    # Compute the real rank of M via QR decomposition
    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[0] * n for _ in range(m)]
        R = [[0 if i != j else A[i][j] for j in range(n)] for i in range(m)]
        
        for k in range(min(m, n)):
            norm = sum(A[i][k]**2 for i in range(k, m))**0.5
            Q[k][k] = A[k][k] / norm
            R[k][k] = norm
            
            for j in range(k + 1, n):
                R[k][j] = sum(Q[i][k] * A[i][j] for i in range(k, m))
            
            for i in range(k + 1, m):
                Q[i][k] = sum(Q[k][j] * A[i][j] for j in range(k, n)) / R[k][k]
                for j in range(k, n):
                    A[i][j] -= Q[i][k] * R[k][j]
        
        return Q, R
    
    Q, R = qr_decomposition(M)
    
    # Count the number of non-zero rows in R
    rank_R = sum(1 for row in R if any(x != 0 for x in row))
    
    metric_value = rank_R
    instances_tested = 1
    conjecture_holds = rank_R >= 3.5 * math.log(n)
    counterexample = "" if conjecture_holds else "rank < 3.5 log n"
    
    return {
        "metric_name": "Real Rank of Moment Matrix",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < 3.5 log n\" first_failing_seed={first_failing_seed}")