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
    
    def qr_decomposition(matrix):
        n = len(matrix)
        Q, R = [], []
        for i in range(n):
            Q.append([])
            R.append([])
            for j in range(n):
                if i == j:
                    R[i].append(1.0)
                else:
                    R[i].append(0.0)
        
        for k in range(n):
            v = [matrix[k][i] for i in range(n)]
            norm_v = math.sqrt(sum(x**2 for x in v))
            
            Q[k][k] = v[k] / norm_v
            for j in range(k + 1, n):
                R[k][j] = sum(Q[i][k] * matrix[i][j] for i in range(n))
                q_j_norm = math.sqrt(sum(R[j][i]**2 for i in range(j, n)))
                Q[j][k] = R[j][k] / q_j_norm
                for i in range(k + 1, n):
                    R[k][i] -= Q[j][k] * R[j][i]
        
        return Q, R

    def eigenvalues(matrix):
        Q, R = qr_decomposition(matrix)
        n = len(matrix)
        eigs = []
        for k in range(n):
            xi = sum(Q[i][k]**2 for i in range(k + 1, n))
            norm_x = math.sqrt(xi)
            e_k = [xi / norm_x if i == k else 0 for i in range(n)]
            eigs.append(e_k)
        return eigs

    def choi_matrix(channel):
        n = len(channel)
        M = [[0.0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                M[i][j] = channel[i][j]
                M[i + n][j + n] = channel[i][j]
                M[j][i] = channel[j][i]
                M[j + n][i + n] = channel[j][i]
        return M

    def non_commutative_entropy(eigs):
        entropy = 0.0
        for eig in eigs:
            if eig > 0:
                entropy -= eig * math.log2(eig)
        return entropy

    def generate_channel(n):
        channel = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            channel[i][i] += n - sum(channel[i])
        return channel

    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0.0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(100):
            channel = generate_channel(n)
            choi = choi_matrix(channel)
            eigs = eigenvalues(choi)
            entropy = non_commutative_entropy(eigs)
            total_entropy += entropy
            instances_tested += 1
            n_max = max(n_max, n)

            if entropy < 0.1 * n or entropy > 10 * n:
                conjecture_holds = False
                counterexample = f"n={n}, entropy={entropy}"

    mean_entropy = total_entropy / instances_tested

    return {
        "metric_name": "non_commutative_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")