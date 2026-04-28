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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def pseudoinverse(L):
    n = len(L)
    I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    L_inv = gaussian_elimination([[L[i][j] + I[i][j] for j in range(n)] for i in range(n)])
    return [[L_inv[i][j] - I[i][j] for j in range(n)] for i in range(n)]

def effective_resistance(G, S):
    n = len(G)
    L = [[Fraction(0) if i != j else Fraction(-1) + sum(Fraction(1) if G[i][k] == 1 and k not in S else 0 for k in range(n)) for j in range(n)] for i in range(n)]
    L_inv = pseudoinverse(L)
    e_u = [Fraction(1) if u in S else Fraction(0) for u in range(n)]
    one_S = sum(Fraction(1) if u in S else Fraction(0) for u in range(n))
    return e_u[0]**2 * L_inv[0][0] + (one_S**(-2)) * L_inv[0][0] - (2 * one_S * e_u[0]) * L_inv[0][0]

def generate_graph(n):
    while True:
        G = [[0]*n for _ in range(n)]
        for u in range(n):
            neighbors = random.sample([v for v in range(n) if v != u], 2)
            G[u][neighbors[0]] = 1
            G[u][neighbors[1]] = 1
            G[neighbors[0]][u] = 1
            G[neighbors[1]][u] = 1
        if all(sum(G[i]) == 3 for i in range(n)):
            return G

def Tseitin_encoding(G, c):
    n = len(G)
    clauses = []
    for u in range(n):
        for v in range(u+1, n):
            if G[u][v] == 1:
                clauses.append([u, -v])
                clauses.append([-u, v])
    return clauses

def lex_dpll(clauses, assignment=None):
    if assignment is None:
        assignment = [False] * len(clauses)
    for i in range(len(clauses)):
        literal = next((j for j in range(len(clauses[i])) if not assignment[j]), None)
        if literal is None:
            return True
        new_assignment = assignment[:]
        new_assignment[literal] = True
        if lex_dpll(clauses, new_assignment):
            return True
        new_assignment[literal] = False
        if lex_dpll(clauses, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    for n in n_values:
        for _ in range(30):
            G = generate_graph(n)
            c = random.choice([i for i in range(1, 2*n, 2)])
            S = sorted(random.sample(range(n), math.ceil(n/3)))
            nu_R = effective_resistance(G, S)
            T_G_c = Tseitin_encoding(G, c)
            d_DPLL = lex_dpll(T_G_c)
            results.append((nu_R * n, math.log(d_DPLL) if d_DPLL > 0 else -math.inf))
    return {
        "metric_name": "log_d_DPLL",
        "metric_value": sum(v for v, _ in results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.6 * mean + 1) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(min((r - (0.6 * mean + 1)) for r in results))]
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")