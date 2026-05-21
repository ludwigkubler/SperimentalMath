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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(2 * n):
            bp.append(random.choice([0, 1]))
        return bp
    
    def construct_transition_matrix(bp):
        n = len(bp) // 2
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            if bp[2 * i] == 0:
                M[i][i + 1] += 1
            else:
                M[i][i] += 1
            if bp[2 * i + 1] == 0:
                M[i + 1][i + 1] += 1
            else:
                M[i + 1][i] += 1
        return M
    
    def max_singular_value(M):
        n = len(M)
        U, S, Vt = svd(M)
        return max(S)
    
    def svd(A):
        m, n = len(A), len(A[0])
        A_t = [[A[j][i] for j in range(m)] for i in range(n)]
        Q, R = qr_decomposition(A)
        Q_t = [[Q[j][i] for j in range(m)] for i in range(m)]
        S = [[R[i][i] if i < n else 0 for i in range(n)] for _ in range(n)]
        Vt = [[R[i][j] / R[i][i] if i == j and i < n else 0 for j in range(n)] for i in range(n)]
        return Q_t, S, Vt
    
    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[A[j][i] / math.sqrt(sum(A[k][i]**2 for k in range(m))) if j == i else 0 for j in range(m)] for i in range(n)]
        R = [[sum(Q[j][k] * A[k][l] for k in range(min(j + 1, n))) for l in range(n)] for j in range(m)]
        return Q, R
    
    def frobenius_norm(A):
        m, n = len(A), len(A[0])
        norm = 0
        for i in range(m):
            for j in range(n):
                norm += A[i][j]**2
        return math.sqrt(norm)
    
    def power_iteration(A, max_iter=100):
        m, n = len(A), len(A[0])
        x = [random.random() for _ in range(n)]
        x /= frobenius_norm(x)
        for _ in range(max_iter):
            y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
            y /= frobenius_norm(y)
            x = y
        return frobenius_norm(A @ x) / frobenius_norm(x)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    bp = generate_read_twice_bp(n)
    M = construct_transition_matrix(bp)
    max_sing_val = max_singular_value(M)
    log_n = math.log(n)
    
    return {
        "metric_name": "max_singular_value",
        "metric_value": max_sing_val,
        "instances_tested": 1,
        "conjecture_holds": max_sing_val >= n,
        "counterexample": "" if max_sing_val >= n else f"n={n}, max_sing_val={max_sing_val}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < n for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={r['metric_value']}, max_sing_val={r['metric_value']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")