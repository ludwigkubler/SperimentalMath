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
    
    def gram_schmidt(A):
        Q, R = [], []
        for a in A:
            q = [x for x in a]
            for u in Q:
                r = sum(q[i] * u[i] for i in range(len(a)))
                for j in range(len(u)):
                    q[j] -= r * u[j]
            norm = math.sqrt(sum(x**2 for x in q))
            if norm == 0:
                continue
            R.append([q[i] / norm for i in range(len(q))])
            Q.append([x / norm for x in q])
        return Q, R
    
    def matrix_rank(A):
        Q, _ = gram_schmidt(A)
        rank = sum(1 for row in Q if any(x != 0 for x in row))
        return rank
    
    def sos_relaxation(d, A):
        n = len(A)
        M = [[0] * (n + d) for _ in range(n + d)]
        for i in range(n):
            for j in range(i, n):
                M[i][j] = M[j][i] = A[i][j]
        for k in range(d):
            for i in range(n):
                for j in range(i, n):
                    M[n + k][n + k] += 2 * M[i][j] * M[i][j]
                    M[n + k][i] -= M[j][j]
                    M[n + k][j] -= M[i][i]
        return matrix_rank(M)
    
    def max_cut_approximation(A):
        n = len(A)
        x = [random.choice([-1, 1]) for _ in range(n)]
        cut_value = sum(max(0, A[i][j] * (x[i] + x[j])) for i in range(n) for j in range(i+1, n))
        return cut_value
    
    def sos_degree_required(A):
        n = len(A)
        target_ratio = 0.878
        for d in range(1, 11):
            if sos_relaxation(d, A) >= max_cut_approximation(A) * target_ratio:
                return d
        return float('inf')
    
    def adjacency_matrix(n):
        A = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[j][i] = A[i][j]
        return A
    
    n = random.randint(40, 50)
    A = adjacency_matrix(n)
    real_rank = matrix_rank(A)
    sos_deg = sos_degree_required(A)
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_deg,
        "instances_tested": 1,
        "conjecture_holds": sos_deg >= real_rank,
        "counterexample": "" if sos_deg >= real_rank else f"Graph with n={n}, A={A}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n}, A={A}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")