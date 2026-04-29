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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = max(range(rank, m), key=lambda i: abs(A[i][j]))
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def log2(x):
        return math.log2(x)
    
    def canonical_clique_dnf(n, k):
        terms = []
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        for clique in itertools.combinations(edges, k):
            term = [0] * len(edges)
            for edge in clique:
                term[edges.index(edge)] = 1
            terms.append(term)
        return terms
    
    def random_poly_dnf(n, m, w):
        terms = []
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        edge_set = set(random.sample(edges, min(m // w, len(edges))))
        for _ in range(m):
            term = [0] * len(edges)
            selected_edges = random.sample(edge_set, w)
            for edge in selected_edges:
                term[edges.index(edge)] = 1
            terms.append(term)
        return terms
    
    def delta(F, N):
        m = len(F)
        rho_2 = gaussian_elimination(F)
        return log2(m + 1) - log2(rho_2 + 1)
    
    n_values = [6, 8, 10, 12]
    k_values = [3, 4, lambda n: n // 2]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for k in k_values:
            if callable(k):
                k = k(n)
            F_clique = canonical_clique_dnf(n, k)
            F_random = random_poly_dnf(n, n, 2) + random_poly_dnf(n, n**2, 3) + random_poly_dnf(n, n * math.floor(math.log(n)), math.floor(math.log(n)))
            
            for F in [F_clique] + F_random:
                instances_tested += 1
                delta_F = delta(F, n)
                
                if k == n // 2 and n >= 6:
                    if delta_F < n / 2 - 3 * math.log2(n) - 4:
                        conjecture_holds = False
                        counterexample = f"n={n}, k={k}, Δ(F^{n,k})={delta_F}"
                
                if n == 8 and len(F_random) > 0:
                    F1, F2 = random.sample(F_random, 2)
                    delta_F1 = delta(F1, n)
                    delta_F2 = delta(F2, n)
                    delta_F_and = delta([t for t in F1 if any(t[i] == 1 for i in range(len(t)))], n)
                    delta_F_or = max(delta_F1, delta_F2)
                    
                    if delta_F_and > delta_F1 + delta_F2 + 1:
                        conjecture_holds = False
                        counterexample = f"n=8, Δ(F∧G)={delta_F_and}, Δ(F)+Δ(G)+1={delta_F1+delta_F2+1}"
                    
                    if delta_F_or > max(delta_F1, delta_F2) + 1:
                        conjecture_holds = False
                        counterexample = f"n=8, Δ(F∨G)={delta_F_or}, max(Δ(F),Δ(G))+1={max(delta_F1,delta_F2)+1}"
    
    return {
        "metric_name": "Delta",
        "metric_value": delta_F,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")