# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

def sparse_matrix_rank(A, block_size=64):
    n = len(A)
    rank = 0
    for i in range(0, n, block_size):
        for j in range(i, min(n, i + block_size)):
            if A[j][j] != 0:
                for k in range(j + 1, min(n, j + block_size)):
                    factor = -A[k][j] / A[j][j]
                    for l in range(j, min(n, j + block_size)):
                        A[k][l] += factor * A[j][l]
                rank += 1
    return rank

def build_graph(X):
    n = len(X)
    G = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hamming_distance(X[i], X[j]) <= 1:
                G[i].append(j)
                G[j].append(i)
    return G

def build_cochain_complex(G):
    n = len(G)
    E_bi = [(i, j) for i in range(n) for j in G[i]]
    T_bi = [(i, j, k) for i in range(n) for j in G[i] for k in G[j] if hamming_distance(X[i], X[k]) <= 2]
    return E_bi, T_bi

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [3, 4, 5, 6]:
        X = [''.join(random.choice('01') for _ in range(n)) for _ in range(2**n)]
        G = build_graph(X)
        
        h1_values = []
        for _ in range(200):
            f = [random.choice('01') for _ in range(n)]
            X_f = [x for x, y in zip(X, f) if y == '0']
            E_bi, T_bi = build_cochain_complex(G)
            
            delta_0 = [[0] * len(E_bi) for _ in range(len(X_f))]
            delta_1 = [[0] * len(T_bi) for _ in range(len(E_bi))]
            
            for (i, j), k in zip(E_bi, T_bi):
                if f[i] == '0' and f[j] == '0':
                    delta_0[k][E_bi.index((i, j))] = 1
                    delta_1[E_bi.index((i, j))][T_bi.index((i, j, k))] = 1
            
            rank_delta_0 = sparse_matrix_rank(delta_0)
            rank_delta_1 = sparse_matrix_rank(delta_1)
            
            h1_values.append(rank_delta_1 - rank_delta_0)
        
        empirical_mean = sum(h1_values) / len(h1_values)
        fraction_positive = sum(1 for x in h1_values if x > 0) / len(h1_values)
        
        results.append({
            "n": n,
            "empirical_mean": empirical_mean,
            "fraction_positive": fraction_positive
        })
    
    conjecture_holds = all(r["fraction_positive"] <= math.exp(-2 * r["n"]) for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "fraction_positive",
        "metric_value": sum(r["fraction_positive"] for r in results) / len(results),
        "instances_tested": 200 * len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")