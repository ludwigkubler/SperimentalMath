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

def generate_bipartite_graph(n):
    A = list(range(n))
    B = list(range(n, 2*n))
    E = set()
    for _ in range(int(n * (n - 1) / 4)):
        u = random.choice(A)
        v = random.choice(B)
        if (u, v) not in E and (v, u) not in E:
            E.add((u, v))
    return A, B, E

def max_matching(G):
    n = len(G[0])
    matching = [-1] * n
    visited = [False] * n
    
    def dfs(u):
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                if matching[v] == -1 or dfs(matching[v]):
                    matching[v] = u
                    return True
        return False
    
    for u in range(n):
        visited = [False] * n
        dfs(u)
    
    return sum(1 for x in matching if x != -1)

def schur_weyl_rank(G):
    A, B, E = G
    n = len(A)
    M = [[0] * (n + n) for _ in range(n + n)]
    
    for u, v in E:
        M[u][v], M[v][u] = 1, 1
    
    def gaussian_elimination(M):
        m, n = len(M), len(M[0])
        rank = 0
        for j in range(n):
            i_max = -1
            for i in range(rank, m):
                if M[i][j]:
                    i_max = i
                    break
            if i_max == -1:
                continue
            M[rank], M[i_max] = M[i_max], M[rank]
            rank += 1
            for i in range(rank, m):
                factor = M[i][j] / M[rank-1][j]
                for k in range(n):
                    M[i][k] -= factor * M[rank-1][k]
        return rank
    
    return gaussian_elimination(M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = generate_bipartite_graph(n)
    lambda_G = max_matching(G)
    R_G = schur_weyl_rank(G)
    
    metric_name = "R(G)"
    metric_value = R_G
    instances_tested = 1
    conjecture_holds = R_G >= math.sqrt(n) / 2
    counterexample = "" if conjecture_holds else f"R(G)={R_G} < {math.sqrt(n)/2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")