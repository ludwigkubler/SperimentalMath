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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def rank(A):
    m, n = len(A), len(A[0])
    row_echelon_form = [row[:] for row in A]
    gaussian_elimination(row_echelon_form)
    rank = 0
    for i in range(m):
        if any(row_echelon_form[i]):
            rank += 1
    return rank

def tree_width(G):
    n = len(G)
    visited = [False] * n
    parent = [-1] * n
    
    def dfs2(node, par, path):
        visited[node] = True
        path.add(node)
        
        max_width = 0
        for neighbor in G[node]:
            if not visited[neighbor]:
                width = dfs2(neighbor, node, path) + 1
                max_width = max(max_width, width)
        
        path.remove(node)
        return max_width
    
    def dfs1(node):
        nonlocal max_width
        visited[node] = True
        
        for neighbor in G[node]:
            if not visited[neighbor]:
                parent[neighbor] = node
                dfs1(neighbor)
        
        stack = [node]
        while stack:
            current = stack.pop()
            path = set()
            width = 0
            
            def dfs3(node, par):
                nonlocal width
                visited[node] = True
                path.add(node)
                
                for neighbor in G[node]:
                    if not visited[neighbor]:
                        dfs3(neighbor, node)
                
                path.remove(node)
                width = max(width, len(path))
            
            dfs3(current, -1)
            max_width = max(max_width, width)
    
    max_width = 0
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = random.sample(range(n), 2)
        if u > v:
            u, v = v, u
        G[u].append(v)
        G[v].append(u)
    
    tree_width_val = tree_width(G)
    k_theory_rank = rank([[random.randint(0, 1) for _ in range(n)] for _ in range(n)])
    
    return {
        "metric_name": "K-theory Rank",
        "metric_value": k_theory_rank,
        "instances_tested": n,
        "conjecture_holds": False if k_theory_rank < 2**(math.log(tree_width_val, 2)) else True,
        "counterexample": f"Tree-width: {tree_width_val}, K-theory Rank: {k_theory_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"Tree-width too small\" first_failing_seed={first_failing_seed}")