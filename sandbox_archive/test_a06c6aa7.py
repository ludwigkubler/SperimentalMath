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
    
    def generate_ramanujan_graph(n):
        # Configuration model to generate a 3-regular graph
        G = [[] for _ in range(n)]
        degrees = [0] * n
        while any(d != 3 for d in degrees):
            u, v = random.sample(range(n), 2)
            if u not in G[v] and v not in G[u]:
                G[u].append(v)
                G[v].append(u)
                degrees[u] += 1
                degrees[v] += 1
        return G
    
    def generate_planted_separator_graph(n):
        # Two K3,3 blocks joined by a small bridge
        G = [[] for _ in range(6)]
        G[0], G[1], G[2] = [1, 3, 4], [0, 2, 5], [1, 2]
        G[3], G[4], G[5] = [0, 5], [0, 4], [1, 4]
        return G
    
    def generate_cycle_gadgets_graph(n):
        # Cycle of K4 gadgets
        G = [[] for _ in range(4 * n)]
        for i in range(n):
            G[4 * i] = [4 * (i + 1) % (4 * n), 4 * (i - 1) % (4 * n), 4 * i + 1, 4 * i + 2]
            G[4 * i + 1] = [4 * i, 4 * (i + 1) % (4 * n), 4 * i + 3]
            G[4 * i + 2] = [4 * i, 4 * (i - 1) % (4 * n), 4 * i + 3]
            G[4 * i + 3] = [4 * i, 4 * (i + 1) % (4 * n)]
        return G
    
    def walsh_hadamard_transform(f):
        n = len(f)
        for s in range(1, n):
            mask = 1 << s
            for i in range(n // (2 ** s)):
                for j in range(2 ** s):
                    f[i * (2 ** s) + j] += f[i * (2 ** s) + j + mask]
        return f
    
    def compute_f_hat(G, sigma):
        n = len(G)
        f_hat = [0] * (1 << n)
        for i in range(1 << n):
            S = [j for j in range(n) if i & (1 << j)]
            count = sum(len([v for v in G[j] if v not in S]) <= len(G) // 3 for j in S)
            f_hat[i] = (-1) ** count
        return walsh_hadamard_transform(f_hat)
    
    def compute_nu(G):
        n = len(G)
        f_hat = compute_f_hat(G, [0] * n)
        nu = -math.log2(sum(f_hat[i] ** 2 for i in range(1 << (n // 8 + 1)))) - math.log2(1 / sum(abs(f_hat[i]) for i in range(1 << n)) + 1)
        return nu
    
    def compute_log2_L_R(G, sigma):
        # Simple DPLL refutation count for Tseitin formula
        n = len(sigma)
        stack = [(0, [])]
        decisions = 0
        while stack:
            i, assignment = stack.pop()
            if i == n:
                return math.log2(decisions)
            if assignment[i] is None:
                assignment[i] = 0
                stack.append((i + 1, assignment[:]))
                assignment[i] = 1
                stack.append((i + 1, assignment[:]))
            else:
                decisions += 1
        return math.log2(decisions)
    
    def generate_instance(n):
        if n == 10: return generate_ramanujan_graph(10)
        elif n == 12: return generate_planted_separator_graph(12)
        elif n == 14: return generate_cycle_gadgets_graph(14)
        else: raise ValueError("Unsupported graph type")
    
    def run_experiment(n):
        G = generate_instance(n)
        sigma = [random.randint(0, 1) for _ in range(len(G))]
        nu = compute_nu(G)
        log2_L_R = compute_log2_L_R(G, sigma)
        return {
            "metric_name": "nu_G",
            "metric_value": nu,
            "instances_tested": 1,
            "conjecture_holds": nu >= n / 4 and log2_L_R >= nu / 12,
            "counterexample": "" if nu < n / 4 or log2_L_R >= nu / 12 else f"nu_G={nu}, log2(L_R)={log2_L_R}"
        }
    
    results = [run_experiment(n) for n in {10, 12, 14}]
    mean_nu = sum(r["metric_value"] for r in results) / len(results)
    std_nu = math.sqrt(sum((r["metric_value"] - mean_nu) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_nu": mean_nu,
        "std_nu": std_nu,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_nu = sum(r["mean_nu"] for r in results) / len(results)
    std_nu = math.sqrt(sum((r["mean_nu"] - mean_nu) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["support_fraction"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_nu} std={std_nu} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if r["support_fraction"] < 0.8), None)
        print(f"RESULT: FALSIFIED counterexample='support_fraction<0.8' first_failing_seed={first_failing_seed}")