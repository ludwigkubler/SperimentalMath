# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_3_regular(G):
        degree = [0] * len(G)
        for u in range(len(G)):
            degree[u] = sum(1 for v in G[u] if v > u)
        return all(d == 3 for d in degree)
    
    def configuration_model(n, m):
        G = [[] for _ in range(n)]
        edges = set()
        while len(edges) < m:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u].append(v)
                G[v].append(u)
                edges.add((u, v))
        return G
    
    def hashimoto_matrix(G):
        E = [(u, v) for u in range(len(G)) for v in G[u] if v > u]
        n = len(E)
        B = [[0] * (2*n) for _ in range(2*n)]
        for i, (u, v) in enumerate(E):
            j = E.index((v, u))
            B[2*i][2*j+1] = 1
            B[2*i+1][2*j] = 1
        return B
    
    def eigenvalues(matrix):
        n = len(matrix)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A = matrix
        Q, R = [], []
        for _ in range(n):
            Q.append(A[0])
            r = [A[i][0] / A[0][0] for i in range(1, n)]
            R.append(r)
            A = [[A[i][j] - sum(Q[k][j] * R[k][i] for k in range(i)) for j in range(n)] for i in range(1, n)]
        Q = [q / q[0] for q in Q]
        R = [r / r[0] for r in R]
        eigenvals = []
        while len(eigenvals) < n:
            max_eigval = -float('inf')
            for i in range(n):
                if all(abs(Q[i][j]) < 1e-9 for j in range(i+1, n)):
                    eigval = Q[i][i]
                    eigenvals.append(eigval)
                    Q = [[Q[j][k] - eigval * Q[j][i] * Q[i][k] / Q[i][i] for k in range(n)] for j in range(n)]
                    break
            else:
                raise ValueError("Matrix is not diagonalizable")
        return eigenvals
    
    def lexicographic_dpll(G, sigma):
        n = len(G)
        stack = [(0, 0)]
        solved = False
        cap = 2**22
        while not solved and len(stack) < cap:
            u, i = stack[-1]
            if i == len(G[u]):
                stack.pop()
            else:
                v = G[u][i]
                if sigma[v] == 0:
                    stack.append((v, 0))
                elif sigma[v] == 1:
                    solved = True
        return solved
    
    def tseitin_encoding(G, sigma):
        n = len(G)
        clauses = []
        for u in range(n):
            for v in G[u]:
                if sigma[v] == 0:
                    clauses.append([-(u+1), -(v+1)])
                elif sigma[v] == 1:
                    clauses.append([(u+1), (v+1)])
        return clauses
    
    def count_leaves(clauses, cap):
        n = len(clauses)
        stack = [(0, 0)]
        solved = False
        while not solved and len(stack) < cap:
            u, i = stack[-1]
            if i == len(clauses[u]):
                stack.pop()
            else:
                clause = clauses[u][i]
                if all(abs(x) in [1, -1] for x in clause):
                    solved = True
                else:
                    stack.append((u, i+1))
        return solved
    
    def generate_graph(n):
        while True:
            G = configuration_model(n, n*3)
            if is_3_regular(G):
                return G
    
    def compute_nu(G):
        B = hashimoto_matrix(G)
        eigenvals = sorted(eigenvalues(B), reverse=True)
        lambda2 = eigenvals[1]
        nu = n * max(0, (2**0.5 - (lambda2 - 2**0.5)) / 2**0.5) / 2**0.5
        return nu
    
    def run_dpll(G, sigma):
        clauses = tseitin_encoding(G, sigma)
        cap = 2**22
        solved = count_leaves(clauses, cap)
        if not solved:
            return False, cap
        else:
            return True, None
    
    n_values = [12, 16, 20, 24, 28]
    trials = 30
    support_threshold = 0.85
    rho_threshold = 0.6
    total_trials = len(n_values) * trials
    nu_respecting_count = 0
    log2T_values = []
    
    for n in n_values:
        for _ in range(trials):
            G = generate_graph(n)
            sigma = [random.choice([0, 1]) for _ in range(n)]
            solved, cap = run_dpll(G, sigma)
            nu = compute_nu(G)
            log2T = Fraction(cap).log(2) if cap is not None else 0
            log2T_values.append((n, log2T, nu))
            if solved or (cap is not None and log2T >= nu / 16):
                nu_respecting_count += 1
    
    support_fraction = nu_respecting_count / total_trials
    rho = 0.0
    
    uncapped_trials = [(n, log2T, nu) for n, log2T, nu in log2T_values if cap is not None]
    if len(uncapped_trials) > 0:
        from scipy.stats import spearmanr
        _, rho = spearmanr([log2T for n, log2T, nu in uncapped_trials], [nu for n, log2T, nu in uncapped_trials])
    
    result = {
        "metric_name": "log2T/ν(G)",
        "metric_value": sum(log2T / nu for n, log2T, nu in log2T_values) / len(log2T_values),
        "instances_tested": total_trials,
        "conjecture_holds": support_fraction >= support_threshold and rho >= rho_threshold,
        "counterexample": "" if support_fraction >= support_threshold and rho >= rho_threshold else "log₂T < ν/16 − 2"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
    
    log2T_values = [log2T for n, log2T, nu in log2T_values]
    support_fraction = sum(nu_respecting_count / total_trials)
    rho = 0.0
    
    uncapped_trials = [(n, log2T, nu) for n, log2T, nu in log2T_values if cap is not None]
    if len(uncapped_trials) > 0:
        from scipy.stats import spearmanr
        _, rho = spearmanr([log2T for n, log2T, nu in uncapped_trials], [nu for n, log2T, nu in uncapped_trials])
    
    result = {
        "metric_name": "log2T/ν(G)",
        "metric_value": sum(log2T / nu for n, log2T, nu in log2T_values) / len(log2T_values),
        "instances_tested": total_trials,
        "conjecture_holds": support_fraction >= support_threshold and rho >= rho_threshold,
        "counterexample": "" if support_fraction >= support_threshold and rho >= rho_threshold else "log₂T < ν/16 − 2"
    }
    
    print(f"RESULT: {'SUPPORTED' if result['conjecture_holds'] else 'FALSIFIED'} mean={result['metric_value']} std=0.0 support_fraction={support_fraction}")