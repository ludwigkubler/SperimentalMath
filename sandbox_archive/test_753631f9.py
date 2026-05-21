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
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def kruskal(edges):
        edges.sort(key=lambda x: x[2])
        parent = list(range(n))
        
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]
        
        mst_edges = []
        for u, v, w in edges:
            pu, pv = find(u), find(v)
            if pu != pv:
                parent[pu] = pv
                mst_edges.append((u, v, w))
        return mst_edges
    
    def persistence_entropy(M):
        n = len(M)
        distances = []
        for i in range(n):
            for j in range(i + 1, n):
                distances.append(hamming_distance(M[i], M[j]))
        
        if not distances:
            return 0
        
        freqs = {}
        total_weight = sum(distances)
        for d in distances:
            if d > 0:
                if d not in freqs:
                    freqs[d] = 0
                freqs[d] += 1
        
        pe = -sum(Fraction(freqs[d], total_weight) * math.log2(Fraction(freqs[d], total_weight)) for d in freqs)
        return pe
    
    def rank_real(M):
        n, m = len(M), len(M[0])
        M_copy = [row[:] for row in M]
        
        def gaussian_elimination(A):
            rows, cols = len(A), len(A[0])
            rank = 0
            for j in range(cols):
                pivot_row = -1
                for i in range(rank, rows):
                    if A[i][j] != 0:
                        pivot_row = i
                        break
                if pivot_row == -1:
                    continue
                
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                
                for i in range(rank, rows):
                    factor = A[i][j] / A[pivot_row][j]
                    for k in range(j, cols):
                        A[i][k] -= factor * A[pivot_row][k]
            
            return rank
        
        rank = gaussian_elimination(M_copy)
        return rank
    
    def generate_matrix(family, n, r=None):
        if family == 'bernoulli':
            return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        elif family == 'gaussian':
            A = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
            B = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
            return [[int(round(a * b)) for a, b in zip(row_A, row_B)] for row_A, row_B in zip(A, B)]
        elif family == 'sylvester_hadamard':
            if n not in [8, 16, 32]:
                raise ValueError("n must be 8, 16, or 32 for Sylvester-Hadamard matrix")
            H = [[1] * (i + 1) for i in range(n)]
            for j in range(1, n):
                for k in range(j):
                    H[j][k] = -H[k][j]
            return H
        elif family == 'circulant':
            row = [random.choice([-1, 1]) for _ in range(n)]
            return [row[i:] + row[:i] for i in range(n)]
        elif family == 'hadamard_blocks':
            block_size = n // 2
            H = [[1 if (i // block_size) % 2 == (j // block_size) % 2 else -1 for j in range(block_size)] for i in range(block_size)]
            return [row * 4 for row in H]
        else:
            raise ValueError("Unknown matrix family")
    
    n_values = [8, 16, 24, 32]
    results = []
    
    for n in n_values:
        for _ in range(5):
            M = generate_matrix(random.choice(['bernoulli', 'gaussian', 'sylvester_hadamard', 'circulant', 'hadamard_blocks']), n)
            pe = persistence_entropy(M)
            rank = rank_real(M)
            if 2 ** pe > rank + 1:
                results.append((n, pe, rank, True))
            else:
                results.append((n, pe, rank, False))
    
    metric_value = sum(pe for _, pe, _, _ in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(not holds for _, _, _, holds in results)
    counterexample = "" if all(holds for _, _, _, holds in results) else "2^PE > rank + 1"
    
    return {
        "metric_name": "Persistence Entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"2^PE > rank + 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")