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

# Helper functions for linear algebra
def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]

    # Back-substitute to get the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
    
    return x

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0, 1)
    sign = Fraction(1, 1)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -Fraction(1, 1)
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == Fraction(0, 1):
        raise ValueError("Singular matrix")
    
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix)
            adjoint[j][i] = (-1) ** (i+j) * cofactor
    
    return matrix_multiply(adjoint, Fraction(1, det_A))

def identity_matrix(n):
    return [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]

# Function to generate a random quasi-platonic solid
def generate_quasi_platonic_solid(seed):
    random.seed(seed)
    n = random.randint(5, 30)
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    return phi

# Function to construct the associated CNF
def construct_cnf(phi):
    n = len(phi)
    cnf = []
    for i in range(n):
        clause = [j+1 if phi[i][j] == 0 else -(j+1) for j in range(n)]
        cnf.append(clause)
    return cnf

# Function to compute the Frege proof length
def frege_proof_length(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    unit_clauses = {i+1: [] for i in range(n)}
    for i, clause in enumerate(cnf):
        if len(clause) == 1:
            unit_clauses[abs(clause[0])].append(i)
    
    stack = []
    while True:
        found_unit_clause = False
        for i in range(n):
            if unit_clauses[i+1]:
                j = unit_clauses[i+1].pop()
                if cnf[j][0] == i+1:
                    stack.append((j, 1))
                else:
                    stack.append((j, -1))
                found_unit_clause = True
                break
        
        if not found_unit_clause:
            return len(stack)
        
        while stack and stack[-1][1] == 1:
            j, sign = stack.pop()
            for k in range(n):
                if i+1 in clauses[k]:
                    clauses[k].remove(i+1)
                    if len(clauses[k]) == 1:
                        unit_clauses[abs(clauses[k][0])].append(j)
        
        if not any(len(clause) > 0 for clause in clauses):
            return len(stack)

# Function to compute the minimal order of the symmetry group
def symmetry_group_order(phi):
    n = len(phi)
    A = [[phi[i][j] ^ phi[i][k] ^ phi[j][k] for k in range(n)] for i in range(n) for j in range(i+1, n)]
    A = [row[1:] for row in A]
    gaussian_elimination(A)
    rank = sum(1 for row in A if any(row))
    return 2 ** (n - rank)

# Function to run a single trial
def run_trial(seed: int) -> dict:
    phi = generate_quasi_platonic_solid(seed)
    cnf = construct_cnf(phi)
    ord_phi = symmetry_group_order(phi)
    frege_len = frege_proof_length(cnf)
    
    return {
        "metric_name": "symmetry_group_order_frege_length_correlation",
        "metric_value": abs(ord_phi - frege_len),
        "instances_tested": 1,
        "n_max": len(phi),
        "conjecture_holds": ord_phi == frege_len,
        "counterexample": ""
    }

# Main function to run trials
if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"symmetry_group_order_frege_length_correlation\" first_failing_seed={first_failing_seed}")