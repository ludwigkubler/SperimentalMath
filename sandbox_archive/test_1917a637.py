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

def generate_ramanujan_graph(n):
    # Configuration model for Ramanujan-like graph
    degrees = [3] * n
    adjacency_list = [[] for _ in range(n)]
    while any(d > 0 for d in degrees):
        u, v = random.sample(range(n), 2)
        if u != v and len(adjacency_list[u]) < 3 and len(adjacency_list[v]) < 3:
            adjacency_list[u].append(v)
            adjacency_list[v].append(u)
            degrees[u] -= 1
            degrees[v] -= 1
    return adjacency_list

def generate_planted_separator_graph(n):
    # Two K_{3,3}-blocks joined by a small bridge
    G = [[2, 3], [0, 3], [0, 1], [1, 2]]
    for _ in range(n - 4):
        u, v = random.sample(range(4, n), 2)
        if u != v and len(G[u]) < 3 and len(G[v]) < 3:
            G[u].append(v)
            G[v].append(u)
    return G

def generate_poor_expander_graph(n):
    # Cycle of K_4 gadgets
    G = [[1, 2], [0, 2], [0, 1], [3, 4], [2, 5], [4, 6], [5, 7], [6, 8], [7, 9], [8, 10], [9, 11], [10, 11]]
    for _ in range(n - 12):
        u, v = random.sample(range(12, n), 2)
        if u != v and len(G[u]) < 3 and len(G[v]) < 3:
            G[u].append(v)
            G[v].append(u)
    return G

def walsh_hadamard_transform(f):
    n = len(f)
    for s in range(1, n):
        for t in range(n):
            if (t & s) == 0:
                f[t] += f[s ^ t]
                f[s ^ t] -= f[t]
    return [f[i] * math.sqrt(2 / n) for i in range(n)]

def compute_f_hat(G, sigma):
    n = len(G)
    f = [sigma[v] if v < n else 0 for v in range(2 * n)]
    f_hat = walsh_hadamard_transform(f)
    return f_hat

def compute_v_nu(G, f_hat):
    n = len(G)
    k = n // 8
    W_le_k = sum(f_hat[1 << s] ** 2 for s in range(k + 1))
    E_f_G = sum(f_hat[1 << s] for s in range(n)) / (1 << n)
    return -math.log2(W_le_k) - math.log2(1 / E_f_G + 1)

def compute_L_R(G, sigma):
    # Simple DPLL refutation count
    def dpll(G, assignment, clause_count):
        if not G:
            return clause_count
        u = next(v for v in range(len(G)) if len(G[v]) > 0)
        for v in G[u]:
            new_G = [g[:] for g in G]
            new_G[v].remove(u)
            if assignment[v] == 0:
                new_assignment = assignment[:]
                new_assignment[v] = 1
                clause_count += sum(1 for c in G[v] if all(new_assignment[var] == 1 for var in c))
                result = dpll(new_G, new_assignment, clause_count)
                if result is not None:
                    return result
            else:
                new_assignment = assignment[:]
                new_assignment[v] = -1
                clause_count += sum(1 for c in G[v] if all(new_assignment[var] == 1 for var in c))
                result = dpll(new_G, new_assignment, clause_count)
                if result is not None:
                    return result
        return None

    n = len(G)
    sigma_extended = [sigma[v] if v < n else 0 for v in range(2 * n)]
    assignment = [0] * n
    clause_count = sum(1 for c in G if all(sigma[var] == 1 for var in c))
    return dpll(G, assignment, clause_count)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18]
    results = []
    
    for n in n_values:
        for _ in range(30):
            if n == 10:
                G = generate_ramanujan_graph(n)
            elif n == 12:
                G = generate_planted_separator_graph(n)
            else:
                G = generate_poor_expander_graph(n)
            
            sigma = [random.choice([0, 1]) for _ in range(n)]
            f_hat = compute_f_hat(G, sigma)
            v_nu = compute_v_nu(G, f_hat)
            L_R = compute_L_R(G, sigma)
            
            results.append({
                "n": n,
                "v_nu": v_nu,
                "L_R": L_R
            })
    
    mean_v_nu = sum(r["v_nu"] for r in results) / len(results)
    std_v_nu = math.sqrt(sum((r["v_nu"] - mean_v_nu) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["L_R"] >= (1/12) * r["v_nu"]) / len(results)
    
    return {
        "metric_name": "log2_L_R",
        "metric_value": math.log2(L_R),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, v_nu={results[0]['v_nu']}, L_R={results[0]['L_R']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")