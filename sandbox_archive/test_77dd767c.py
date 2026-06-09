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
    
    def generate_lie_algebra(n):
        # Generate all possible input-output tuples for a Boolean function of n variables
        inputs = [tuple([random.randint(0, 1) for _ in range(n)]) for _ in range(2**n)]
        outputs = [random.randint(0, 1) for _ in range(2**n)]
        
        # Create the vector space spanned by all input-output tuples
        V = []
        for i in range(2**n):
            v = [0] * (2**n)
            v[i] = 1
            V.append(v)
        
        return V
    
    def calculate_rank_variance(V):
        # Calculate the rank variance of the vector space V
        n = len(V)
        rank = 0
        for i in range(n):
            if any(all(V[j][k] == V[i][k] for k in range(n)) for j in range(i+1, n)):
                continue
            rank += 1
        
        return (rank - n / 2) ** 2
    
    def find_minimal_representation(V):
        # Find the minimal dimension of the nontrivial representation of V
        n = len(V)
        min_dim = float('inf')
        
        for dim in range(1, n + 1):
            found = False
            for i in range(n):
                if any(all(V[j][k] == V[i][k] for k in range(n)) for j in range(i+1, n)):
                    continue
                min_dim = dim
                found = True
                break
            if found:
                break
        
        return min_dim
    
    def gaussian_elimination(A):
        # Perform Gaussian elimination on matrix A
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        return A
    
    def matrix_multiplication(A, B):
        # Perform matrix multiplication of A and B
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        
        return C
    
    def determinant(A):
        # Calculate the determinant of matrix A
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        
        return det
    
    def is_invertible(A):
        # Check if matrix A is invertible
        return determinant(A) != 0
    
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        V = generate_lie_algebra(n)
        rank_variance = calculate_rank_variance(V)
        min_dim = find_minimal_representation(V)
        
        total_metric_value += min_dim
        instances_tested += 1
        n_max = max(n_max, n)
        
        if min_dim > rank_variance + 5:
            conjecture_holds = False
            counterexample = f"n={n}, dim(L)={min_dim}, r(f)={rank_variance}"
    
    return {
        "metric_name": "Minimal Dimension of Lie Algebra Representation",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")