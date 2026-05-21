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
    edges = [(random.choice(vertices), random.choice(vertices)) for _ in range(int(n * (n - 1) / 2))]
    cut = {v: random.choice([0, 1]) for v in vertices}
    
    # Construct the degree-d pseudoexpectation moment matrix M
    M = [[0] * n for _ in range(n)]
    for u, v in edges:
        if cut[u] != cut[v]:
            M[u][v] += 1
            M[v][u] += 1
    
    # Compute the real rank of M via QR decomposition
    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[0] * n for _ in range(m)]
        R = [[0 if i != j else A[i][j] for j in range(n)] for i in range(m)]
        
        for k in range(n):
            norm = sum(A[i][k]**2 for i in range(k, m))**0.5
            Q[k][k] = 1 / norm
            R[k][k] = norm
            
            for j in range(k + 1, n):
                R[k][j] = sum(A[i][k] * A[i][j] for i in range(k, m))
                Q[j][k] = R[k][j]
                
                for i in range(k, m):
                    A[i][j] -= Q[k][i] * R[k][j]
        
        return Q, R
    
    Q, R = qr_decomposition(M)
    rank = sum(1 for r in R if any(r[j] != 0 for j in range(n)))
    
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
            "counterexample": f"Rank {rank} is less than 3.5 log n"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value
    total_metric_value = sum(res["metric_value"] for res in results if "metric_value" in res)
    instances_tested = sum(res["instances_tested"] for res in results)
    mean_metric_value = total_metric_value / instances_tested
    
    std_metric_value = 0
    for res in results:
        if "metric_value" in res:
            std_metric_value += (res["metric_value"] - mean_metric_value) ** 2
    std_metric_value = (std_metric_value / instances_tested) ** 0.5
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for res in results if "conjecture_holds" in res and res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than 3.5 log n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")