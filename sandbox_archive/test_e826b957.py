# auto-injected by SEC sandbox
import math
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
import cmath

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(m)]
        return C
    
    def dft(M):
        n = len(M)
        M_hat = [[0] * n for _ in range(n)]
        for j in range(n):
            for i in range(n):
                sum_val = 0
                for v in range(n):
                    sum_val += M[i][v] * cmath.exp(2j * cmath.pi * j * v / n)
                M_hat[j][i] = sum_val
        return M_hat
    
    def count_nonzero_entries(M):
        n = len(M)
        count = 0
        for i in range(n):
            for j in range(n):
                if abs(M[i][j]) > 1e-9:
                    count += 1
        return count
    
    def generate_k_clique_dnf(n, k):
        edges = [(i, j) for i in range(1, n+1) for j in range(i+1, n+1)]
        clique_edges = random.sample(edges, k)
        dnf = []
        for edge in clique_edges:
            term = [f"e{i}_{j}" if (i, j) == edge else f"¬e{i}_{j}" for i in range(1, n+1) for j in range(i+1, n+1)]
            dnf.append("∨".join(term))
        return "∧".join(dnf)
    
    def generate_random_dnf(n):
        terms = []
        for _ in range(random.randint(2, 5)):
            term = [f"e{i}_{j}" if random.choice([True, False]) else f"¬e{i}_{j}" for i in range(1, n+1) for j in range(i+1, n+1)]
            terms.append("∨".join(term))
        return "∧".join(terms)
    
    def compute_M(F):
        n = len(F[0])
        M = [[0] * n for _ in range(len(F))]
        for i, term in enumerate(F):
            for v in range(n):
                count = sum(1 for e in term.split("∨") if f"e{v+1}_{v+2}" in e or f"¬e{v+1}_{v+2}" in e)
                M[i][v] = count
        return M
    
    def is_k_clique_dnf(F, n, k):
        for term in F.split("∧"):
            edges = set()
            for e in term.split("∨"):
                if "e" in e:
                    u, v = map(int, e[1:].split("_"))
                    edges.add((u, v))
            if len(edges) != k or any(u > n or v > n for u, v in edges):
                return False
        return True
    
    def is_k_clique_computing(F, n, k):
        M = compute_M([F])
        M_hat = dft(M)
        count = count_nonzero_entries(M_hat)
        return count >= n // 2
    
    n_values = [6, 8, 10, 12, 12, 16, 20]
    k_values = [3, 3, 3, 3, 4, 4, 4]
    
    results = []
    for n, k in zip(n_values, k_values):
        if n < 2 * k or k < 3:
            continue
        
        canonical_dnf = generate_k_clique_dnf(n, k)
        random_dnf = generate_random_dnf(n)
        
        for _ in range(30):
            F = canonical_dnf
            if not is_k_clique_computing(F, n, k):
                results.append({"metric_name": "μ", "metric_value": 0, "instances_tested": 1, "conjecture_holds": False, "counterexample": "not_k_clique"})
                continue
            
            M = compute_M([F])
            M_hat = dft(M)
            count = count_nonzero_entries(M_hat)
            results.append({"metric_name": "μ", "metric_value": count / (n // 2), "instances_tested": 1, "conjecture_holds": True, "counterexample": ""})
        
        for _ in range(30):
            F = random_dnf
            M = compute_M([F])
            M_hat = dft(M)
            count = count_nonzero_entries(M_hat)
            results.append({"metric_name": "μ", "metric_value": count / (n // 2), "instances_tested": 1, "conjecture_holds": False, "counterexample": ""})
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_k_clique\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(3, 34)]
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")