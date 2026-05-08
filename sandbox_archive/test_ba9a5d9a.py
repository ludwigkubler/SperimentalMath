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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3_regular_graph(n):
        G = [[] for _ in range(n)]
        degree = 3
        edges = set()
        while len(edges) < n * degree // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                G[u].append(v)
                G[v].append(u)
                edges.add((u, v))
        return G
    
    def generate_dumbbell_graph():
        K4 = [0, 1, 2, 3]
        M = [(0, 4), (1, 5), (2, 6), (3, 7)]
        bridge = random.choice(K4)
        G = [[] for _ in range(8)]
        for u, v in K4:
            G[u].append(v)
            G[v].append(u)
        for u, v in M:
            G[u].append(v)
            G[v].append(u)
        G[bridge].append(8)
        G[8].append(bridge)
        return G
    
    def generate_cycle_with_chords(n):
        G = [[] for _ in range(n)]
        for i in range(n):
            G[i].append((i + 1) % n)
            G[(i + 1) % n].append(i)
        chords = random.sample(range(n), n // 2)
        for u, v in chords:
            if u != (v + 1) % n and v != (u + 1) % n:
                G[u].append(v)
                G[v].append(u)
        return G
    
    def edge_product_threshold(G):
        n = len(G)
        f_G = [random.choice([-1, 1]) for _ in range(n)]
        sign_sum = sum(f_G[u] * f_G[v] if (u, v) in G or (v, u) in G else 0 for u in range(n) for v in range(u + 1, n))
        return math.copysign(1, sign_sum)
    
    def influence(G, v):
        n = len(G)
        f_G = [random.choice([-1, 1]) for _ in range(n)]
        original_value = edge_product_threshold(G)
        flipped_value = edge_product_threshold(G[:v] + [-f_G[v]] + G[v+1:])
        return abs(original_value - flipped_value)
    
    def estimate_nu_KKL(G):
        n = len(G)
        total_inf = sum(influence(G, v) for v in range(n))
        max_inf = max(influence(G, v) for v in range(n))
        return total_inf / max_inf
    
    def Tseitin_resolution(G, sigma):
        n = len(G)
        clauses = []
        for u, v in G:
            clauses.append([u + 1, -v - 1])
            clauses.append([-u - 1, v + 1])
        for i in range(n):
            if sigma == i:
                clauses.append([i + 1])
            else:
                clauses.append([-i - 1])
        
        def dpll(clauses, assignment):
            unsatisfied = [c for c in clauses if not any(l in assignment and assignment[l] == 1 or -l in assignment and assignment[-l] == 0 for l in c)]
            if not unsatisfied:
                return True
            unit_clauses = [c[0] for c in unsatisfied if len(c) == 1]
            if not unit_clauses:
                return False
            literal = random.choice(unit_clauses)
            assignment[literal] = 1
            if dpll(clauses, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = 1
            if dpll(clauses, assignment):
                return True
            return False
        
        assignment = {}
        return len(clauses) if not dpll(clauses, assignment) else len(assignment)
    
    def compute_L_R(G, sigma):
        n = len(G)
        clauses = []
        for u, v in G:
            clauses.append([u + 1, -v - 1])
            clauses.append([-u - 1, v + 1])
        for i in range(n):
            if sigma == i:
                clauses.append([i + 1])
            else:
                clauses.append([-i - 1])
        
        def dpll(clauses, assignment):
            unsatisfied = [c for c in clauses if not any(l in assignment and assignment[l] == 1 or -l in assignment and assignment[-l] == 0 for l in c)]
            if not unsatisfied:
                return True
            unit_clauses = [c[0] for c in unsatisfied if len(c) == 1]
            if not unit_clauses:
                return False
            literal = random.choice(unit_clauses)
            assignment[literal] = 1
            if dpll(clauses, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = 1
            if dpll(clauses, assignment):
                return True
            return False
        
        assignment = {}
        return len(clauses) if not dpll(clauses, assignment) else len(assignment)
    
    families = [generate_3_regular_graph, generate_dumbbell_graph, generate_cycle_with_chords]
    n_values = [8, 10, 12, 14]
    results = []
    for family in families:
        for n in n_values:
            G = family(n)
            nu_KKL_G = estimate_nu_KKL(G)
            L_R_Tseitin = compute_L_R(G, random.choice(range(n)))
            if nu_KKL_G > 12 * math.log2(L_R_Tseitin + 2):
                return {
                    "metric_name": "nu_KKL",
                    "metric_value": nu_KKL_G,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"nu_KKL(G) > 12*log_2(L_R(Tseitin(G,sigma))+2)"
                }
            results.append({
                "metric_name": "log2_L_R",
                "metric_value": math.log2(L_R_Tseitin),
                "instances_tested": 1,
                "nu_KKL_G": nu_KKL_G
            })
    
    rho = 0.55
    for result in results:
        rho += (result["metric_value"] - math.log2(result["nu_KKL_G"])) / len(results)
    rho /= len(results)
    
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.55,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
    else:
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")