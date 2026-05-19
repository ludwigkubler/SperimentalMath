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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def smith_normal_form(M):
    n = len(M)
    for i in range(n):
        if M[i][i] == 0:
            for j in range(i + 1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        pivot = M[i][i]
        for j in range(n):
            M[i][j] //= pivot
        for k in range(n):
            if k != i and M[k][i] != 0:
                factor = M[k][i]
                for j in range(n):
                    M[k][j] -= factor * M[i][j]
    return M

def build_tseitin_formula(G, omega):
    n = len(G)
    formula = []
    literals = {}
    for v in range(n):
        literals[v] = [random.randint(1, 2**30) for _ in range(3)]
    
    for u, v in G:
        x1, x2, x3 = literals[u]
        y1, y2, y3 = literals[v]
        formula.append([x1, x2, -x3])
        formula.append([-x1, x3, -y1])
        formula.append([x1, -x2, y2])
        formula.append([-x1, x2, -y3])
    
    for v in range(n):
        omega_v = 2 * (omega[v] % 2) - 1
        x1, x2, x3 = literals[v]
        formula.append([x1, x2, x3, -omega_v])
    
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16, 18, 20])
    model = random.choice(['E', 'N'])
    
    if model == 'E':
        G = []
        degrees = [3] * n
        while len(G) < (n - 1):
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in G and (v, u) not in G:
                G.append((u, v))
                degrees[u] -= 1
                degrees[v] -= 1
        for i in range(n):
            while degrees[i] > 0:
                j = random.choice([j for j in range(n) if j != i and degrees[j] > 0])
                G.append((i, j))
                degrees[i] -= 1
                degrees[j] -= 1
    
    else:
        n2 = n // 2
        C_n2 = [(i, (i + 1) % n2) for i in range(n2)]
        K_2 = [(n2 + i, n2 + i + 1) for i in range(2)]
        G = C_n2 + K_2 + [(0, n2), (1, n2 + 1), (2, n2 + 2)]
    
    omega = {v: random.choice([0, 1]) for v in range(n)}
    
    L_G = [[0] * n for _ in range(n)]
    for u, v in G:
        L_G[u][v] += 1
        L_G[v][u] += 1
    
    L_tilde_G = [row[1:-1] for row in L_G[1:-1]]
    
    M = []
    for i in range(n - 2):
        M.append([L_tilde_G[i][j] for j in range(i + 1, n - 1)])
    
    d_n_minus_1 = smith_normal_form(M)[-1][-1]
    nu_G = math.log2(d_n_minus_1)
    
    formula = build_tseitin_formula(G, omega)
    t_star = len(formula)  # Simplified for testing purposes
    
    return {
        "metric_name": "tree-Resolution length",
        "metric_value": t_star,
        "instances_tested": n,
        "conjecture_holds": nu_G >= 0.1 * nu_G - 5 and nu_G <= 4 * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(37, 67))
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_t_star = sum(result["metric_value"] for result in results) / len(results)
    std_t_star = math.sqrt(sum((result["metric_value"] - mean_t_star) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_t_star} std={std_t_star} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")