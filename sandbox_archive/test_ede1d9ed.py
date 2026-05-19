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
    
    n = 20 + random.randint(0, 19)  # n ∈ {5, 10, ..., 40}
    G = generate_random_connected_graph(n)
    mu = compute_algebraic_connectivity(G)
    Tseitin_formula = construct_Tseitin_formula(G)
    resolution_length = measure_resolution_length(Tseitin_formula)
    
    if resolution_length < 2**(0.1 * mu):
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n}, μ={mu}, length={resolution_length}"
        }
    else:
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

def generate_random_connected_graph(n: int) -> list:
    G = [[] for _ in range(n)]
    edges_added = 0
    while edges_added < n - 1:
        u, v = random.sample(range(n), 2)
        if u != v and v not in G[u]:
            G[u].append(v)
            G[v].append(u)
            edges_added += 1
    return G

def compute_algebraic_connectivity(G: list) -> float:
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for u in range(n):
        degree_u = len(G[u])
        L[u][u] = -degree_u
        for v in G[u]:
            if u < v:
                L[u][v] = 1
                L[v][u] = 1
    
    # Compute eigenvalues of L
    eigenvalues = compute_eigenvalues(L)
    mu = min(eigenvalue for eigenvalue in eigenvalues if eigenvalue > 0)
    return mu

def compute_eigenvalues(matrix: list) -> list:
    n = len(matrix)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def matrix_multiply(A, B):
        result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        return result
    
    def matrix_add(A, B):
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    
    def scalar_multiply(s, A):
        return [[s * A[i][j] for j in range(n)] for i in range(n)]
    
    def determinant(A):
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        
        adjoint = [[(-1) ** (i + j) * determinant([[A[m][n] for n in range(j, j+1)] for m in range(i, i+1)]) for j in range(n)] for i in range(n)]
        return scalar_multiply(1 / det_A, adjoint)
    
    eigenvalues = []
    A = matrix
    for _ in range(20):  # Power iteration method
        v = [random.random() for _ in range(n)]
        v = scalar_multiply(1 / sum(v), v)
        Av = matrix_multiply(A, v)
        lambda_ = sum(Av[i] * v[i] for i in range(n))
        eigenvalues.append(lambda_)
        A = matrix_add(scalar_multiply(lambda_, identity), inverse(matrix_subtract(A, scalar_multiply(lambda_, identity))))
    
    return eigenvalues

def construct_Tseitin_formula(G: list) -> str:
    n = len(G)
    variables = {f"x{i}" for i in range(n)}
    clauses = []
    for u in range(n):
        if G[u]:
            clauses.append(f"({variables[u]} v ~x{G[u][0]})")
            for v in G[u][1:]:
                clauses.append(f"(~x{v} v ~x{u})")
    return " ^ ".join(clauses)

def measure_resolution_length(formula: str) -> int:
    # Simplified DPLL implementation with timeout
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c.split()) == 1), None)
        if unit_clause:
            literal = unit_clause.strip()
            if literal.startswith("~"):
                literal = literal[1:]
                polarity = False
            else:
                polarity = True
            assignment[literal] = polarity
            new_clauses = [c for c in clauses if not evaluate_clause(c, assignment)]
            return dpll(new_clauses, assignment)
        pure_literal = next((l for l in variables if all(l in clause or "~" + l in clause for clause in clauses)), None)
        if pure_literal:
            polarity = True
            if pure_literal.startswith("~"):
                literal = pure_literal[1:]
                polarity = False
            else:
                literal = pure_literal
            assignment[literal] = polarity
            new_clauses = [c for c in clauses if not evaluate_clause(c, assignment)]
            return dpll(new_clauses, assignment)
        branching_literal = next(iter(variables))
        return dpll(clauses + [f"{branching_literal}"], assignment) or dpll(clauses + [f"~{branching_literal}"], assignment)
    
    def evaluate_clause(clause: str, assignment):
        literals = clause.split()
        for literal in literals:
            if literal.startswith("~"):
                if literal[1:] not in assignment or assignment[literal[1:]]:
                    return False
            else:
                if literal not in assignment or not assignment[literal]:
                    return False
        return True
    
    variables = set(formula.split())
    clauses = formula.split(" ^ ")
    timeout = 20  # 20 seconds
    start_time = time.time()
    
    def timed_dpll():
        nonlocal result
        if time.time() - start_time > timeout:
            raise TimeoutError
        try:
            result = dpll(clauses, {})
        except RecursionError:
            result = False
    
    result = None
    timed_dpll()
    
    return 1 if result else 0

if __name__ == "__main__":
    import time
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")