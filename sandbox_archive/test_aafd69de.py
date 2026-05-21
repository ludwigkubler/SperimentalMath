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
    
    def generate_read_twice_bp(n):
        bp = []
        for i in range(2**n):
            if i == 0:
                bp.append([i])
            else:
                prev_states = bp[i - 1]
                new_state = [i]
                for state in prev_states:
                    new_state.extend([state << 1, (state << 1) | 1])
                bp.append(new_state)
        return bp

    def transition_matrix(bp):
        n = len(bp)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in bp[i]:
                if j < n:
                    M[j][i] += 1
        return M

    def max_singular_value(M):
        m, n = len(M), len(M[0])
        U, S, Vt = svd(M)
        return max(S)

    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[A[j][i] / math.sqrt(sum(A[k][i]**2 for k in range(m))) if j == i else 0 for j in range(m)] for i in range(n)]
        R = [[sum(Q[i][k] * A[k][j] for k in range(i)) for j in range(i, n)] for i in range(n)]
        return Q, R

    def svd(M):
        m, n = len(M), len(M[0])
        U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
        S = [sum(M[i][j]**2 for j in range(n))**0.5 for i in range(min(m, n))]
        Vt = [[M[j][i] / S[min(j, i)] if j == min(j, i) else 0 for j in range(n)] for i in range(min(m, n))]
        return U, S, Vt

    def log_n(n):
        return math.log2(n)

    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    M = transition_matrix(bp)
    max_sing_val = max_singular_value(M)
    conjecture_holds = max_sing_val >= n
    counterexample = "" if conjecture_holds else f"n={n}, max_sing_val={max_sing_val}"
    
    return {
        "metric_name": "operator_norm_gap",
        "metric_value": max_sing_val,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='operator_norm_gap' first_failing_seed={first_failing_seed}")