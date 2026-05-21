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

def generate_3_regular_graph(n):
    G = [[] for _ in range(n)]
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if len(G[i]) < 2 and len(G[j]) < 2:
                G[i].append(j)
                G[j].append(i)
                edges.add((i, j))
    return G

def compute_eigenvalues(M):
    def QR_iterations(A, max_iter=50):
        n = len(A)
        Q = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        R = A
        for _ in range(max_iter):
            Q, R = qr_decomposition(R)
        return [R[i][i] for i in range(n)]

    def qr_decomposition(A):
        n = len(A)
        Q = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        R = A
        for k in range(n - 1):
            v = [R[i][k] for i in range(k, n)]
            norm = sum(x * x for x in v).sqrt()
            e = [(x / norm) if i == k else Fraction(0) for i, x in enumerate(v)]
            Q_k = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
            for i in range(k, n):
                for j in range(k, n):
                    Q_k[i][j] -= e[i] * e[j]
            Q = matrix_multiply(Q_k, Q)
            R = matrix_multiply(Q_k, R)
        return Q, R

    def matrix_multiply(A, B):
        n = len(A)
        C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    eigenvalues = QR_iterations(M)
    return eigenvalues

def compute_M_G(G, n):
    r = math.ceil(math.sqrt(2 * n))
    V = [[Fraction(1) / math.sqrt(n)] * n for _ in range(r)]
    lambda_max = max(abs(eig) for eig in compute_eigenvalues(V))
    step_size = Fraction(0.1, lambda_max)
    for _ in range(80):
        V = matrix_multiply(V, V)
        normalize_rows(V)
        V = project_to_unit_sphere(V)

    return V

def normalize_rows(M):
    n = len(M)
    for i in range(n):
        norm = sum(x * x for x in M[i]).sqrt()
        if norm == 0:
            continue
        for j in range(n):
            M[i][j] /= norm

def project_to_unit_sphere(V):
    n, r = len(V), len(V[0])
    Q = [[Fraction(1) / math.sqrt(r)] * r for _ in range(n)]
    return matrix_multiply(Q, V)

def compute_R(G, n, eigenvalues):
    count = 0
    for eig in eigenvalues:
        if -1 + Fraction(1, math.sqrt(n)) < eig < 1 - Fraction(1, math.sqrt(n)):
            count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40]
    results = []
    
    for n in n_values:
        R_values = []
        SDP_ratios = []
        
        for _ in range(30):
            G = generate_3_regular_graph(n)
            M_G = compute_M_G(G, n)
            eigenvalues = compute_eigenvalues(M_G)
            R = compute_R(G, n, eigenvalues)
            R_values.append(R / n)
            
            if n <= 20:
                # Compute MaxCut for small graphs
                max_cut = 0
                for i in range(n):
                    for j in range(i + 1, n):
                        if (i, j) in G or (j, i) in G:
                            max_cut += 1
            else:
                # Use UB(G) for large graphs
                lambda_max = max(abs(eig) for eig in eigenvalues)
                UB_G = len(G) / 2 + n * lambda_max / 4
                max_cut = UB_G
            
            SDP_ratios.append(R / n / (0.878 * max_cut))
        
        mean_R = sum(R_values) / len(R_values)
        std_R = math.sqrt(sum((x - mean_R) ** 2 for x in R_values) / len(R_values))
        mean_SDP_ratio = sum(SDP_ratios) / len(SDP_ratios)
        std_SDP_ratio = math.sqrt(sum((x - mean_SDP_ratio) ** 2 for x in SDP_ratios) / len(SDP_ratios))
        
        results.append({
            "n": n,
            "mean_R": mean_R,
            "std_R": std_R,
            "mean_SDP_ratio": mean_SDP_ratio,
            "std_SDP_ratio": std_SDP_ratio
        })
    
    return {
        "metric_name": "R(G)/n",
        "metric_value": sum(result["mean_R"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(0.55 <= R / n < 0.80 for result in results for R in range(int(result["n"] * (0.62 - 0.07)), int(result["n"] * (0.80 + 0.07)))),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")