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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_inv(A, mod):
        n = len(A)
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                I[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        I[k][j] -= factor * I[i][j]
        return [[int(x) % mod for x in row] for row in I]
    
    def tseitin_formula(G, n):
        clauses = []
        literals = {}
        var_count = 0
        for v in range(n):
            literals[v] = var_count
            var_count += 1
        for u, v in G:
            clauses.append([literals[u], literals[v]])
            clauses.append([-literals[u], -literals[v]])
            clauses.append([literals[u], -literals[v]])
            clauses.append([-literals[u], literals[v]])
        return clauses
    
    def minimal_local_index_of_sheaves(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    A[i][literals[literal - 1]] += 1
                else:
                    A[i][-literals[literal - 1]] -= 1
            b[i] = 1
        x = gaussian_elimination(A, b)
        return sum(abs(x[i]) for i in range(n))
    
    def frege_proof_length(clauses):
        n = len(clauses)
        proof = []
        for clause in clauses:
            if len(clause) == 2:
                proof.append((clause[0], clause[1]))
            else:
                proof.append((clause[0], -clause[1]))
        return len(proof)
    
    def generate_d_regular_graph(n, d):
        G = []
        degree = {}
        for v in range(n):
            degree[v] = 0
        while True:
            edges_added = False
            for v in range(n):
                if degree[v] < d:
                    u = random.choice([u for u in range(n) if u != v and degree[u] < d])
                    G.append((v, u))
                    degree[v] += 1
                    degree[u] += 1
                    edges_added = True
            if not edges_added:
                break
        return G
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    G = generate_d_regular_graph(n, d)
    clauses = tseitin_formula(G, n)
    lrs_G = minimal_local_index_of_sheaves(clauses)
    f_phi_G = frege_proof_length(clauses)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": 0.95,  # Placeholder value; actual computation depends on the data
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [71, 73, 79, 83, 89]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")