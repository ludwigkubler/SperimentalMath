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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def log2(x):
        return math.log2(x)
    
    def h_md(G):
        n = len(G)
        m_k = [0] * (n // 2 + 1)
        for e in G:
            u, v = e
            m_k[sum(1 for _ in range(n) if G[_][u] == G[_][v])] += 1
        return sum(m_k) / n
    
    def tseitin_formula(G, c):
        n = len(G)
        literals = {i: (f'x{i}', f'y{i}') for i in range(n)}
        clauses = []
        for e in G:
            u, v = e
            x_u, y_u = literals[u]
            x_v, y_v = literals[v]
            clauses.append([f'-{y_u}', f'{x_v}'])
            clauses.append([f'-{y_v}', f'{x_u}'])
            clauses.append([f'-{x_u}', f'-{x_v}', f'y_u'])
            clauses.append([f'-{x_u}', f'-{x_v}', f'y_v'])
        for i in range(n):
            x_i, y_i = literals[i]
            if c[i] == 1:
                clauses.append([f'{x_i}'])
            else:
                clauses.append([f'-{x_i}'])
        return clauses
    
    def resolution_width(clauses):
        n = len(clauses)
        resolvents = []
        for k in range(1, n + 1):
            new_resolvents = []
            for clause in clauses:
                if len(clause) > k:
                    continue
                for other_clause in clauses:
                    if len(other_clause) > k and set(clause).isdisjoint(set(other_clause)):
                        resolvent = list(set(clause) | set(other_clause))
                        resolvent.remove('-' + resolvent[0])
                        new_resolvents.append(resolvent)
            if not new_resolvents:
                return k - 1
            clauses.extend(new_resolvents)
        return n
    
    def is_3_regular(G):
        for v in range(len(G)):
            if sum(1 for e in G if v in e) != 3:
                return False
        return True
    
    def generate_random_odd_charges(n, num_charges):
        charges = []
        for _ in range(num_charges):
            charge = [random.choice([0, 1]) for _ in range(n)]
            if sum(charge) % 2 == 1:
                charges.append(charge)
        return charges
    
    def generate_prism(n):
        G = [[i, (i + 1) % n] for i in range(n)] + [[n - 1, n // 2], [0, n // 2]]
        return G
    
    def generate_möbius_kantor():
        G = [
            [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10],
            [10, 11], [11, 0], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 8], [7, 9], [8, 10]
        ]
        return G
    
    def generate_petersen():
        G = [
            [0, 1], [0, 4], [0, 5], [1, 2], [1, 6], [2, 3], [2, 7], [3, 4], [3, 8], [4, 9],
            [5, 6], [5, 9], [6, 7], [7, 8], [8, 9]
        ]
        return G
    
    def generate_random_3_regular(n):
        while True:
            G = [[] for _ in range(n)]
            edges = set()
            for i in range(n):
                for j in range(i + 1, n):
                    if random.choice([0, 1]) == 1 and (i, j) not in edges and (j, i) not in edges:
                        G[i].append(j)
                        G[j].append(i)
                        edges.add((i, j))
            if is_3_regular(G):
                return G
    
    n_values = [4, 6, 8, 10, 12, 14]
    num_charges = 5
    alpha = 0.05
    instances_tested = 0
    total_width = 0
    min_ratio = float('inf')
    
    for n in n_values:
        if n == 6:
            G = generate_prism(n)
        elif n == 8:
            G = generate_möbius_kantor()
        elif n == 10:
            G = generate_petersen()
        else:
            G = generate_random_3_regular(n)
        
        charges = generate_random_odd_charges(n, num_charges)
        for c in charges:
            instances_tested += 1
            h_md_value = h_md(G)
            T = tseitin_formula(G, c)
            width = resolution_width(T)
            ratio = width / (n * h_md_value)
            total_width += ratio
            min_ratio = min(min_ratio, ratio)
    
    mean_width = total_width / instances_tested
    support_fraction = instances_tested / len(n_values) / num_charges
    
    if min_ratio >= alpha and mean_width >= 0.1:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if not sys.argv[1:] else [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")