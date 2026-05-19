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
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = 1
                    edges.add((i, j))
        return G, edges
    
    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        degree = [sum(row) for row in G]
        for i in range(n):
            L[i][i] = degree[i]
            for j in range(i + 1, n):
                if G[i][j]:
                    L[i][j] = -1
                    L[j][i] = -1
        return L
    
    def compute_eigenvalues(L):
        n = len(L)
        eigenvalues = []
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        def matrix_multiply(A, B):
            n = len(A)
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        C[i][j] += A[i][k] * B[k][j]
            return C
        
        def scalar_multiply(s, A):
            return [[s * A[i][j] for j in range(n)] for i in range(n)]
        
        def matrix_add(A, B):
            n = len(A)
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    C[i][j] = A[i][j] + B[i][j]
            return C
        
        def identity_matrix(n):
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        def matrix_power(A, k):
            n = len(A)
            result = identity_matrix(n)
            while k > 0:
                if k % 2 == 1:
                    result = matrix_multiply(result, A)
                A = matrix_multiply(A, A)
                k //= 2
            return result
        
        def trace(A):
            return sum(A[i][i] for i in range(n))
        
        def det(A):
            n = len(A)
            if n == 1:
                return A[0][0]
            elif n == 2:
                return A[0][0] * A[1][1] - A[0][1] * A[1][0]
            else:
                det_val = 0
                for j in range(n):
                    submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                    det_val += (-1) ** j * A[0][j] * det(submatrix)
                return det_val
        
        def eigenvector(A, eigenvalue):
            n = len(A)
            B = matrix_subtract(A, scalar_multiply(eigenvalue, identity_matrix(n)))
            for _ in range(100):  # Simple power iteration
                v = [random.random() for _ in range(n)]
                v = normalize(v)
                v_next = matrix_vector_product(B, v)
                if norm(v_next) < 1e-6:
                    return v_next
                v = v_next
            return v
        
        def normalize(v):
            norm_val = norm(v)
            return [x / norm_val for x in v]
        
        def norm(v):
            return math.sqrt(sum(x ** 2 for x in v))
        
        def matrix_subtract(A, B):
            n = len(A)
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    C[i][j] = A[i][j] - B[i][j]
            return C
        
        def matrix_vector_product(A, v):
            n = len(A)
            result = [0] * n
            for i in range(n):
                result[i] = sum(A[i][j] * v[j] for j in range(n))
            return result
        
        # Power iteration to find the largest eigenvalue and corresponding eigenvector
        max_eigenvalue = -math.inf
        max_eigenvector = None
        for _ in range(100):
            v = [random.random() for _ in range(n)]
            v = normalize(v)
            v_next = matrix_vector_product(L, v)
            eigenvalue = norm(v_next) / norm(v)
            if eigenvalue > max_eigenvalue:
                max_eigenvalue = eigenvalue
                max_eigenvector = v_next
        
        # Subtract the largest eigenvalue and find the next largest
        L_sub = matrix_subtract(L, scalar_multiply(max_eigenvalue, identity_matrix(n)))
        second_max_eigenvalue = -math.inf
        for _ in range(100):
            v = [random.random() for _ in range(n)]
            v = normalize(v)
            v_next = matrix_vector_product(L_sub, v)
            eigenvalue = norm(v_next) / norm(v)
            if eigenvalue > second_max_eigenvalue:
                second_max_eigenvalue = eigenvalue
        
        return [max_eigenvalue, second_max_eigenvalue]
    
    def compute_algebraic_connectivity(G):
        L = laplacian_matrix(G)
        eigenvalues = compute_eigenvalues(L)
        mu = min(eigenvalue for eigenvalue in eigenvalues if eigenvalue > 0)
        return mu
    
    def tseitin_formula(G, edges):
        n = len(G)
        literals = [f"x{i+1}" for i in range(n)]
        clauses = []
        
        # Clause for each vertex
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                if G[i][j]:
                    clause.append(f"~{literals[j]}")
            clauses.append(clause)
        
        # Clause for each edge
        for u, v in edges:
            clauses.append([f"{literals[u]}", f"{literals[v]}"])
            clauses.append([f"~{literals[u]}", f"~{literals[v]}"])
        
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            value = literal[0] != '~'
            new_assignment = assignment.copy()
            new_assignment[literal[1:]] = value
            return dpll([c for c in clauses if not any(lit in c for lit in (literal, f"~{literal}"))], new_assignment)
        
        literal = next((l for l in literals if l not in assignment), None)
        if literal:
            new_assignment1 = assignment.copy()
            new_assignment1[literal] = True
            if dpll(clauses, new_assignment1):
                return True
            
            new_assignment2 = assignment.copy()
            new_assignment2[literal] = False
            if dpll(clauses, new_assignment2):
                return True
        
        return False
    
    def resolution_length(clauses):
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                clause_i = clauses[i]
                clause_j = clauses[j]
                if any(lit in clause_i and f"~{lit}" in clause_j for lit in literals):
                    new_clause = [lit for lit in clause_i if lit not in clause_j] + [f"~{lit}" for lit in clause_j if lit not in clause_i]
                    clauses.append(new_clause)
        return len(clauses)
    
    n = random.randint(5, 40)
    G, edges = generate_random_graph(n)
    mu = compute_algebraic_connectivity(G)
    Tseitin_clauses = tseitin_formula(G, edges)
    length = resolution_length(Tseitin_clauses)
    
    c = Fraction(1, 10)
    if length < 2 ** (c * mu):
        return {
            "metric_name": "resolution_length",
            "metric_value": length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n}, μ={mu}, length={length}"
        }
    else:
        return {
            "metric_name": "resolution_length",
            "metric_value": length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")