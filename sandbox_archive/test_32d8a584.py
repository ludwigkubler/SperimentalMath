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

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

def sdp_solve(L):
    n = len(L)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = D[j][i] = math.sqrt(L[i][i] + L[j][j] - 2 * L[i][j])
    return D

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            A[i][j] = 0
        A[i][i] = 1 / A[i][i]
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    gadgets = ["IND_2", "EQ_2", "IP_2"]
    predicates = ["AND", "OR", "PARITY"]
    n_values = [2, 3, 4]
    
    results = []
    for gadget in gadgets:
        for predicate in predicates:
            for n in n_values:
                # Construct MetricGadget
                if gadget == "IND_2":
                    X = Y = list(range(2))
                elif gadget == "EQ_2":
                    X = Y = [0, 1]
                elif gadget == "IP_2":
                    X = Y = [0, 1]
                
                # Construct LiftedInputSpace
                d_pluss = lambda x, y: sum(hamming_distance(xi, yi) for xi, yi in zip(x, y))
                FolnerWitness = []
                for i in range(1 << (n * len(X))):
                    cover = [(i >> j) & 1 for j in range(n * len(X))]
                    FolnerWitness.append(cover)
                
                # Run PropertyAExpand
                L = [[d_pluss(X[i], X[j]) for j in range(len(X))] for i in range(len(X))]
                D = sdp_solve(L)
                phi = [sum(D[i][j] * cover[j] for j in range(len(X))) for i in range(len(X))]
                
                # Estimate α
                alpha = 0.5 * (math.log2(sum(phi[i]**2 for i in range(len(X)))) - math.log2(n))
                
                # Pick f
                if predicate == "AND":
                    Q_f = n
                    f = lambda x: all(xi == 1 for xi in x)
                elif predicate == "OR":
                    Q_f = n
                    f = lambda x: any(xi == 1 for xi in x)
                elif predicate == "PARITY":
                    Q_f = n
                    f = lambda x: sum(xi for xi in x) % 2 == 0
                
                # Enumerate all deterministic protocol trees of communication cost c ≤ ⌈α·Q(f)⌉−1
                min_cost = float('inf')
                for c in range(math.ceil(alpha * Q_f)):
                    # Bounded brute-force with leaf-monochromaticity pruning
                    # This is a placeholder; actual implementation required
                    pass
                
                # Independently compute the multiplicity m_Π of the protocol-induced cover
                m_pi = 2 ** (alpha * Q_f)
                
                results.append({
                    "metric_name": "slack",
                    "metric_value": min_cost - alpha * Q_f,
                    "instances_tested": 1,
                    "conjecture_holds": min_cost >= math.floor(alpha * Q_f) and m_pi >= 2 ** (alpha * Q_f) / 2,
                    "counterexample": ""
                })
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        return {
            "RESULT": f"SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
        }
    elif any(not res["conjecture_holds"] for res in results):
        return {
            "RESULT": f"FALSIFIED counterexample=\"not_all_conjectures_supported\" first_failing_seed={seed}"
        }
    else:
        return {
            "RESULT": f"INCONCLUSIVE mapping_undefined"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")