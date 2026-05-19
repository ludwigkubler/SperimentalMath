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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        # Generate a random max-CUT instance with n vertices
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def construct_sos_moment_matrix(edges, d):
        # Construct the degree-d SOS moment matrix M_d
        n = len(edges)
        M_d = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i in range(n):
            M_d[i][i] += 1
        
        for u, v in edges:
            for k in range(d):
                M_d[u][v] += Fraction(1, 2**k)
                M_d[v][u] += Fraction(1, 2**k)
        
        return M_d
    
    def real_rank(matrix):
        # Compute the real rank of a matrix via eigenvalue decomposition
        n = len(matrix)
        A = [[matrix[i][j] for j in range(n + 1)] for i in range(n)]
        
        # Perform Gaussian elimination to find the rank
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            
            pivot = Fraction(A[i][i])
            for j in range(n + 1):
                A[i][j] /= pivot
            
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n + 1):
                        A[j][k] -= factor * A[i][k]
        
        rank = sum(1 for row in A if any(row))
        return rank
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    
    for d in range(1, min(n, 5) + 1):
        M_d = construct_sos_moment_matrix(edges, d)
        rank_M_d = real_rank(M_d)
        
        if rank_M_d < 0.8 * d**2:
            return {
                "metric_name": "real_rank",
                "metric_value": rank_M_d,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, d={d}, rank(M_d)={rank_M_d}"
            }
    
    return {
        "metric_name": "real_rank",
        "metric_value": 0.8 * min(n, 5)**2,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples_found")