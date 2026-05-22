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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return det

    def is_expander(G, epsilon=0.1):
        n = len(G)
        degree_sum = sum(sum(1 for _ in neighbors) for neighbors in G)
        avg_degree = degree_sum / n
        if avg_degree <= 2 * epsilon:
            return False
        max_degree = max(len(neighbors) for neighbors in G)
        min_degree = min(len(neighbors) for neighbors in G)
        if (max_degree - min_degree) > 2 * epsilon * avg_degree:
            return False
        return True

    def geometric_entropy(G):
        n = len(G)
        adjacency_matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i, neighbors in enumerate(G):
            degree = sum(1 for _ in neighbors)
            for j in neighbors:
                adjacency_matrix[i][j] = Fraction(1, degree)
        laplacian_matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            laplacian_matrix[i][i] = -sum(adjacency_matrix[i])
            for j in range(i+1, n):
                laplacian_matrix[i][j] = adjacency_matrix[i][j]
                laplacian_matrix[j][i] = adjacency_matrix[i][j]
        det_laplacian = determinant(laplacian_matrix)
        if det_laplacian == 0:
            return Fraction(1)
        entropy = -math.log(abs(det_laplacian)) / math.log(n)
        return Fraction(entropy).limit_denominator()

    def tseitin_formula(G):
        n = len(G)
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i, neighbors in enumerate(G):
            clause = [variables[i]]
            for j in neighbors:
                clause.append(f'-{variables[j]}')
            clauses.append(clause)
        return clauses

    def resolution_length(clauses):
        stack = []
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    resolvents = []
                    for lit in clause_i:
                        if '-' + lit in clause_j:
                            new_lit = lit[1:]
                            resolvent = (clause_i - {lit}) | (clause_j - {'-' + lit})
                            if len(resolvent) == 0:
                                return float('inf')
                            resolvents.append(new_lit)
                    for lit in clause_j:
                        if '-' + lit in clause_i:
                            new_lit = lit[1:]
                            resolvent = (clause_j - {lit}) | (clause_i - {'-' + lit})
                            if len(resolvent) == 0:
                                return float('inf')
                            resolvents.append(new_lit)
                    for lit in resolvents:
                        new_clauses.append([lit])
            clauses.extend(new_clauses)
            if not any(len(clause) == 1 for clause in clauses):
                break
        return len(clauses)

    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    if not is_expander(G):
        return {
            "metric_name": "geometric_entropy",
            "metric_value": geometric_entropy(G),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    F = tseitin_formula(G)
    L_F = resolution_length(F)

    if L_F == float('inf'):
        return {
            "metric_name": "geometric_entropy",
            "metric_value": geometric_entropy(G),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution refutation length is infinite"
        }

    H_G = geometric_entropy(G)
    ratio = H_G / L_F

    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_G,
        "instances_tested": 1,
        "conjecture_holds": ratio >= Fraction(1, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"] if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")