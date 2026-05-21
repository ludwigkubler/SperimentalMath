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
    
    def is_k_clique_computing(dnf, k):
        n = len(dnf[0])
        for term in dnf:
            if len(term) != k:
                return False
        return True
    
    def generate_k_clique_dnf(n, k):
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        clique_edges = random.sample(edges, k * (k - 1) // 2)
        dnf = []
        for edge in clique_edges:
            term = [edge[0], edge[1]]
            for other_edge in edges:
                if other_edge != edge and set(other_edge).issubset(set(edge)):
                    term.append(other_edge[0])
                    term.append(other_edge[1])
            dnf.append(term)
        return dnf
    
    def generate_non_k_clique_dnf(n, k):
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        non_clique_edges = [e for e in edges if e not in random.sample(edges, k * (k - 1) // 2)]
        dnf = []
        for edge in non_clique_edges:
            term = [edge[0], edge[1]]
            for other_edge in edges:
                if other_edge != edge and set(other_edge).issubset(set(edge)):
                    term.append(other_edge[0])
                    term.append(other_edge[1])
            dnf.append(term)
        return dnf
    
    def matrix_multiplication(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] for row in matrix]
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[:-1] for row in augmented_matrix]
    
    def dft(M, n):
        m = len(M)
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                sum_val = 0
                for v in range(n):
                    sum_val += M[i][v] * math.cos(2 * math.pi * j * v / n)
                    sum_val -= M[i][v] * math.sin(2 * math.pi * j * v / n) * 1j
                result[i][j] = sum_val
        return result
    
    def cyclic_fourier_spread(M, n):
        m = len(M)
        M_hat = dft(M, n)
        count = sum(abs(entry) > 1e-9 for row in M_hat for entry in row)
        return count
    
    test_cases = [(6, 3), (8, 3), (10, 3), (12, 3), (12, 4), (16, 4), (20, 4)]
    results = []
    
    for n, k in test_cases:
        canonical_dnf = generate_k_clique_dnf(n, k)
        non_k_clique_dnf = generate_non_k_clique_dnf(n, k)
        
        mu_canonical = cyclic_fourier_spread(canonical_dnf, n)
        mu_non_k_clique = cyclic_fourier_spread(non_k_clique_dnf, n)
        
        results.append({
            "n": n,
            "k": k,
            "mu_canonical": mu_canonical,
            "mu_non_k_clique": mu_non_k_clique
        })
    
    mean_mu_canonical = sum(result["mu_canonical"] for result in results) / len(results)
    mean_mu_non_k_clique = sum(result["mu_non_k_clique"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["mu_canonical"] >= n // 2) / len(results)
    
    return {
        "metric_name": "cyclic_fourier_spread",
        "metric_value": mean_mu_canonical,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"n={results[0]['n']}, k={results[0]['k']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_mu_canonical = sum(result["mu_canonical"] for result in results) / len(results)
    mean_mu_non_k_clique = sum(result["mu_non_k_clique"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["mu_canonical"] >= n // 2) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_mu_canonical} std=NA support_fraction={support_fraction}")
    elif any(result["mu_canonical"] < n // 2 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["mu_canonical"] < n // 2)
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['n']}, k={results[0]['k']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")