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
    
    def generate_transition_matrix(n):
        T = []
        for i in range(2):
            row = [0] * (n + 1)
            row[i] = 1
            T.append(row)
        return T

    def transpose(A):
        m, n = len(A), len(A[0])
        A_T = [[A[j][i] for j in range(m)] for i in range(n)]
        return A_T

    def svd(A):
        A_T = transpose(A)
        Q1, R1 = qr_decomposition(A)
        Q2, R2 = qr_decomposition(R1)
        U = transpose(Q2)
        S = [R2[i][i] for i in range(min(len(U), len(S)))]
        V = Q1
        return U, S, V

    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[0] * n for _ in range(m)]
        R = A.copy()
        for i in range(n):
            norm = sum(R[j][i]**2 for j in range(i, m))**0.5
            if norm == 0:
                continue
            Q[i][i] = 1 / norm
            for j in range(i + 1, m):
                Q[j][i] = R[j][i] / norm
            for j in range(m):
                R[j][i:] = [R[j][k] - Q[j][i] * R[i][k] for k in range(i, n)]
        return Q, R

    def sum_of_singular_values(T):
        U, S, V = svd(T)
        return sum(S)

    n = random.randint(5, 40)
    T_twice = generate_transition_matrix(n)
    T_once = generate_transition_matrix(n)  # Placeholder for read-once BP transition matrix

    sv_sum_twice = sum_of_singular_values(T_twice)
    sv_sum_once = sum_of_singular_values(T_once)

    return {
        "metric_name": "Sum of Singular Values",
        "metric_value_twice": sv_sum_twice,
        "metric_value_once": sv_sum_once,
        "instances_tested": 2,
        "conjecture_holds": sv_sum_twice >= n and sv_sum_once <= math.log(n),
        "counterexample": "" if sv_sum_twice >= n and sv_sum_once <= math.log(n) else "n={}".format(n)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean_value_twice = sum(r["metric_value_twice"] for r in results) / len(results)
    mean_value_once = sum(r["metric_value_once"] for r in results) / len(results)

    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean_twice={} std_twice={} support_fraction={}".format(mean_value_twice, math.sqrt(sum((r["metric_value_twice"] - mean_value_twice)**2 for r in results) / len(results)), support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='n={}' first_failing_seed={}".format(result["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")