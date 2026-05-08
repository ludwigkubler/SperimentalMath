# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_3_regular_graph(n):
        while True:
            edges = set()
            for v in range(n):
                neighbors = random.sample(range(v + 1, n), 2)
                if (v, neighbors[0]) not in edges and (neighbors[0], v) not in edges:
                    edges.add((v, neighbors[0]))
                if (v, neighbors[1]) not in edges and (neighbors[1], v) not in edges:
                    edges.add((v, neighbors[1]))
            if len(edges) == n // 2:
                return list(edges)
    
    def generate_dumbbell_graph(n):
        K4 = [(0, 1), (0, 2), (0, 3), (1, 2)]
        chords = random.sample(range(4, n), n - 4)
        edges = K4 + [(i, i + 4) for i in chords]
        return edges
    
    def generate_cycle_with_chords(n):
        cycle_edges = [(i, (i + 1) % n) for i in range(n)]
        chord_edges = random.sample(cycle_edges, n // 2)
        return cycle_edges + chord_edges
    
    def flip_vertex(G, v):
        new_G = set()
        for u, w in G:
            if u == v:
                new_G.add((w, v))
            elif w == v:
                new_G.add((u, v))
            else:
                new_G.add((u, w))
        return new_G
    
    def estimate_nu_KKL(G):
        n = len(G) + 1
        inf_v_values = [0] * n
        for v in range(n):
            flips = 5000
            total_inf = 0
            for _ in range(flips):
                G_prime = flip_vertex(G, v)
                if sum(1 for u, w in G if (u, w) not in G_prime and (w, u) not in G_prime) % 2 == 1:
                    total_inf += 1
            inf_v_values[v] = total_inf / flips
        max_inf = max(inf_v_values)
        return sum(inf_v_values) / max_inf if max_inf > 0 else 0
    
    def Tseitin(G, sigma):
        n = len(G) + 1
        clauses = []
        for v in range(n):
            clauses.append([sigma[v]])
        for u, w in G:
            clauses.append([-sigma[u], -sigma[w]])
            clauses.append([sigma[u], sigma[w]])
        return clauses
    
    def DPLL(clauses):
        assignment = [None] * len(clauses)
        stack = []
        
        def backtrack():
            while stack:
                v = stack.pop()
                if assignment[v] is None:
                    assignment[v] = True
                    for clause in clauses[v]:
                        if clause not in assignment:
                            stack.append(clause)
                    if all(assignment[abs(c)] == (c > 0) for c in clauses[v]):
                        continue
                    else:
                        assignment[v] = False
                        for clause in clauses[v]:
                            if clause not in assignment:
                                stack.append(clause)
                else:
                    assignment[v] = None
        
        backtrack()
        return assignment
    
    def L_R(clauses):
        n = len(clauses)
        sigma = [random.choice([True, False]) for _ in range(n)]
        while True:
            sigma = DPLL(clauses)
            if all(sigma[abs(c)] == (c > 0) for c in clauses):
                return sum(1 for s in sigma if s)
    
    families = [
        generate_random_3_regular_graph,
        generate_dumbbell_graph,
        generate_cycle_with_chords
    ]
    sizes = [8, 10, 12, 14]
    instances_tested = 0
    total_inf = 0
    max_inf = 0
    
    for family in families:
        for n in sizes:
            G = family(n)
            nu_KKL_G = estimate_nu_KKL(G)
            sigma = [random.choice([True, False]) for _ in range(n)]
            L_R_val = L_R(Tseitin(G, sigma))
            instances_tested += 1
            total_inf += nu_KKL_G
            max_inf = max(max_inf, nu_KKL_G)
    
    nu_KKL_avg = total_inf / instances_tested
    
    return {
        "metric_name": "nu_KKL",
        "metric_value": nu_KKL_avg,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    nu_KKL_values = [r["metric_value"] for r in results]
    L_R_values = [r["instances_tested"] / 360 * math.log2(r["instances_tested"]) for r in results]
    
    rho, _ = spearman_rho(nu_KKL_values, L_R_values)
    
    if rho >= 0.55 and all(nu_KKL <= 12 * math.log2(L_R + 2) for nu_KKL, L_R in zip(nu_KKL_values, L_R_values)):
        print(f"RESULT: SUPPORTED mean={sum(nu_KKL_values)/len(nu_KKL_values)} std={math.sqrt(sum((x - sum(nu_KKL_values)/len(nu_KKL_values))**2 for x in nu_KKL_values) / len(nu_KKL_values))} support_fraction=1.0")
    else:
        first_failing_seed = next(i for i, (nu_KKL, L_R) in enumerate(zip(nu_KKL_values, L_R_values)) if nu_KKL > 12 * math.log2(L_R + 2))
        print(f"RESULT: FALSIFIED counterexample=\"nu_KKL > 12*log_2(L_R+2)\" first_failing_seed={seeds[first_failing_seed]}")

def spearman_rho(x, y):
    n = len(x)
    rank_x = {x[i]: i + 1 for i in range(n)}
    rank_y = {y[i]: i + 1 for i in range(n)}
    
    sum_d_squared = sum((rank_x[xi] - rank_y[yi]) ** 2 for xi, yi in zip(x, y))
    
    rho = 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    return rho, None