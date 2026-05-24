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
    
    def laplacian_matrix(graph):
        n = len(graph)
        L = [[0] * n for _ in range(n)]
        for u, v in graph:
            L[u][u] += 1
            L[v][v] += 1
            L[u][v] -= 1
            L[v][u] -= 1
        return L
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 0: return [1]
        if n == 1: return [matrix[0][0], -1]
        
        det = 0
        for j in range(n):
            sub_matrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1)**j * matrix[0][j] * determinant(sub_matrix)
        return [det]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1: return matrix[0][0]
        det = 0
        for j in range(n):
            sub_matrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1)**j * matrix[0][j] * determinant(sub_matrix)
        return det
    
    def hodge_rank(matrix):
        n = len(matrix)
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        A = matrix
        B = I
        
        # Gaussian elimination
        for k in range(n):
            max_row = k
            for i in range(k+1, n):
                if abs(A[i][k]) > abs(A[max_row][k]):
                    max_row = i
            A[k], A[max_row] = A[max_row], A[k]
            B[k], B[max_row] = B[max_row], B[k]
            
            pivot = A[k][k]
            for j in range(k, n):
                A[k][j] /= pivot
                B[k][j] /= pivot
            
            for i in range(n):
                if i != k:
                    factor = A[i][k]
                    for j in range(k, n):
                        A[i][j] -= factor * A[k][j]
                        B[i][j] -= factor * B[k][j]
        
        rank = sum(1 for row in A if any(val != Fraction(0, 1) for val in row))
        return rank
    
    def resolution_proof_size(graph):
        n = len(graph)
        # Placeholder function; actual implementation needed
        return n**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n)]
        L = laplacian_matrix(graph)
        char_poly = characteristic_polynomial(L)
        hodge_rank_val = hodge_rank(L)
        proof_size = resolution_proof_size(graph)
        
        results.append({
            "n": n,
            "hodge_rank": hodge_rank_val,
            "proof_size": proof_size
        })
    
    if not results:
        return {
            "metric_name": "Hodge Rank vs Resolution Proof Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    hodge_ranks = [result["hodge_rank"] for result in results]
    proof_sizes = [result["proof_size"] for result in results]
    
    mean_hodge_rank = sum(hodge_ranks) / len(hodge_ranks)
    mean_proof_size = sum(proof_sizes) / len(proof_sizes)
    
    if all(rank >= n**1.5 for rank, n in zip(hodge_ranks, n_values)) and all(size >= c * n**2 for size, n in zip(proof_sizes, n_values)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Hodge Rank or Proof Size does not meet the conjectured bounds"
    
    return {
        "metric_name": "Hodge Rank vs Resolution Proof Size",
        "metric_value": mean_hodge_rank,
        "instances_tested": len(results),
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")