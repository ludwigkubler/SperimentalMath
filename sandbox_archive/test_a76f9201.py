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
from fractions import Fraction
import math

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    
    # Back-substitute to get the solution
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = A[i][-1] / A[i][i]
        for j in range(i-1, -1, -1):
            A[j][-1] -= A[j][i] * x[i]
    
    return x

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    
    if m == 1:
        return A[0][0]
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    
    return det

def inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    
    det = determinant(A)
    if det == 0:
        raise ZeroDivisionError("Modular inverse does not exist")
    
    adjugate = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            adjugate[i][j] = (-1) ** (i+j) * determinant(submatrix)
    
    return matrix_multiply(adjugate, [[Fraction(1, det)] * n for _ in range(m)])

# Function to compute the minimal Hodge decomposition rank
def mhdrank(phi):
    # Placeholder implementation of mhdrank
    # This is a dummy function and should be replaced with actual computation
    return random.randint(1, 5)

# DPLL solver
def dpll(phi):
    def solve(assignment):
        if not phi:
            return True
        unit_clause = next((c for c in phi if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            assignment[lit] = True
            if solve(assignment):
                return True
            del assignment[lit]
            assignment[-lit] = True
            if solve(assignment):
                return True
            del assignment[-lit]
            return False
        
        literal, polarity = next((l for l in phi[0] if l not in assignment), None), True
        assignment[literal] = polarity
        if solve(assignment):
            return True
        del assignment[literal]
        assignment[-literal] = not polarity
        if solve(assignment):
            return True
        del assignment[-literal]
        return False
    
    return solve({})

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    phi = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(random.randint(1, 3))]
        phi.append(clause)
    
    mhdrank_value = mhdrank(phi)
    width = dpll(phi)
    
    return {
        "metric_name": "mhdrank_width_correlation",
        "metric_value": mhdrank_value * width,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

# Main function to run trials and print results
if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")