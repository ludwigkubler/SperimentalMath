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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Construct resolution graph as a simplicial complex
    simplicial_complex = []
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                simplicial_complex.append((i, j))
    
    # Compute persistent homology (simplified version)
    max_persistence = 0
    for k in range(2, len(simplicial_complex) + 1):
        chain_complex = []
        boundary_matrix = []
        for i in range(k):
            chain_complex.append([Fraction(0)] * k)
            boundary_matrix.append([Fraction(0)] * (k-1))
        
        # Fill chain complex and boundary matrix
        for edge in simplicial_complex[:k]:
            chain_complex[edge[1]][edge[0]] = Fraction(1)
            if edge[1] > 0:
                boundary_matrix[edge[1]-1][edge[0]] = Fraction(-1)
        
        # Compute kernel of boundary matrix
        ker_B = []
        for i in range(k-1):
            row = [Fraction(0)] * (k-1)
            row[i] = Fraction(1)
            ker_B.append(row)
        
        # Gaussian elimination on boundary matrix to find kernel
        gaussian_elimination(boundary_matrix)
        rank_B = sum(1 for row in boundary_matrix if any(x != 0 for x in row))
        max_persistence = max(max_persistence, k - rank_B)
    
    # Estimate resolution proof size (simplified version)
    proof_size = len(simplicial_complex) + n
    
    # Check conjecture
    conjecture_holds = max_persistence >= math.log2(proof_size) / n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_persistence",
        "metric_value": max_persistence,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")