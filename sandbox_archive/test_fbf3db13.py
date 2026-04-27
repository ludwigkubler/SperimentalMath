# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def sign_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def frobenius_norm(M):
    return sum(sum(x**2 for x in row) for row in M)

def energy_gap(M):
    n = len(M)
    if n <= 14:
        partitions = [1 << i for i in range(1, n)]
        max_gap = 0
        for mask in partitions:
            A = [M[i][:] for i in range(n) if (mask & (1 << i)) != 0]
            B = [M[i][:] for i in range(n) if (mask & (1 << i)) == 0]
            gap_A = frobenius_norm(A)
            gap_B = frobenius_norm(B)
            max_gap = max(max_gap, abs(gap_A**2 - gap_B**2))
        return max_gap / n**2
    else:
        # Local search for n=16
        best_gap = 0
        for _ in range(1000):
            mask = random.getrandbits(n)
            A = [M[i][:] for i in range(n) if (mask & (1 << i)) != 0]
            B = [M[i][:] for i in range(n) if (mask & (1 << i)) == 0]
            gap_A = frobenius_norm(A)
            gap_B = frobenius_norm(B)
            best_gap = max(best_gap, abs(gap_A**2 - gap_B**2))
        return best_gap / n**2

def singular_values(M):
    M_T = [list(x) for x in zip(*M)]
    U, S, V = [], [], []
    for i in range(len(M)):
        u = [random.random() for _ in range(len(M))]
        u /= frobenius_norm(u)
        U.append(u)
        s = frobenius_norm([sum(M[j][k] * u[k] for k in range(len(M))) for j in range(len(M))])
        S.append(s)
        v = [M[j][i] / s for j in range(len(M))]
        V.append(v)
    return U, S, V

def rigidity(M, rank):
    n = len(M)
    U, S, V = singular_values(M)
    S_low = sum(S[rank:])
    k = 0
    while True:
        perturbed_M = [[M[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            if random.random() < 0.5:
                perturbed_M[i][k] *= -1
        U_pert, S_pert, V_pert = singular_values(perturbed_M)
        if frobenius_norm([S_pert[j] * U_pert[j] for j in range(rank)]) > frobenius_norm([S_low * U[j] for j in range(rank)]):
            return k
        k += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    results = defaultdict(list)
    
    for n in n_values:
        for _ in range(200):
            M = sign_matrix(n)
            g_M = energy_gap(M)
            U, S, V = singular_values(M)
            s_low_M = sum(S[n//4:])
            R_M_n4 = rigidity(M, n//4)
            delta_M = R_M_n4 / n**2 - (1/16) * max(0, s_low_M - g_M)
            results[n].append(delta_M)
    
    support_fraction = all(delta >= 0 for n in n_values for delta in results[n]) and all(sum(results[n]) / len(results[n]) >= 0 for n in n_values)
    conjecture_holds = support_fraction
    counterexample = "" if support_fraction else "mapping_undefined"
    
    return {
        "metric_name": "delta_M",
        "metric_value": sum(sum(results[n]) / len(results[n]) for n in n_values) / len(n_values),
        "instances_tested": 1200,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_delta_M = sum(result["metric_value"] for result in results.values()) / len(results)
    support_fraction = all(delta >= 0 for n in n_values for delta in results[n]) and all(sum(results[n]) / len(results[n]) >= 0 for n in n_values)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_delta_M} std=0.0 support_fraction=1.0")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[0]}")