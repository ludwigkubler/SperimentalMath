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
    
    def quine_mccluskey(f):
        n = len(f[0])
        minterms = [i for i in range(2**n) if f[i]]
        pi = []
        
        while minterms:
            next_pi = set()
            singletons = {}
            
            for term in minterms:
                for i in range(n):
                    mask = 1 << i
                    neighbor = term ^ mask
                    if neighbor in minterms:
                        if (term, neighbor) not in singletons:
                            singletons[(term, neighbor)] = []
                        singletons[(term, neighbor)].append(term)
            
            for pair, terms in singletons.items():
                next_pi.add(pair[0])
                for t in terms:
                    minterms.remove(t)
            
            pi.extend(next_pi)
        
        return pi

    def is_compatible(p, q):
        for i in range(len(p)):
            if p[i] != 'x' and q[i] != 'x' and p[i] != q[i]:
                return False
        return True

    def build_graph(pi):
        n = len(pi)
        adj = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(i+1, n):
                if is_compatible(pi[i], pi[j]):
                    adj[i][j] = 1
                    adj[j][i] = 1
        
        return adj

    def treewidth(adj):
        n = len(adj)
        if n == 0:
            return -1
        
        def dfs(node, parent, bag):
            nonlocal max_bag_size
            max_bag_size = max(max_bag_size, len(bag))
            
            for neighbor in range(n):
                if adj[node][neighbor] and neighbor != parent:
                    new_bag = set(bag)
                    new_bag.add(neighbor)
                    dfs(neighbor, node, new_bag)
        
        max_bag_size = 0
        dfs(0, -1, {0})
        return max_bag_size - 1

    def sigma_dnf(pi):
        n = len(pi)
        m = len(f)
        cover_matrix = [[0]*m for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                if all(pi[i][k] == 'x' or pi[i][k] == f[j][k] for k in range(n)):
                    cover_matrix[i][j] = 1
        
        def branch_and_bound(row, col, count):
            if row == n:
                return count
            min_count = float('inf')
            
            for j in range(col, m):
                if cover_matrix[row][j]:
                    new_cover_matrix = [row[:] for row in cover_matrix]
                    for i in range(n):
                        if pi[i][row] != 'x' and pi[i][row] == f[j][i]:
                            new_cover_matrix[i][j] = 0
                    min_count = min(min_count, branch_and_bound(row+1, j+1, count + (new_cover_matrix[row].count(1) > 0)))
            
            return min_count
        
        return branch_and_bound(0, 0, 0)

    n = random.choice([6, 8, 10])
    k = 4
    terms = [random.sample(range(n), 3) for _ in range(k)]
    f = [[any(pi[i][j] == 'x' or pi[i][j] == term[j] for j in range(n)) for i in range(2**n)] for term in terms]
    
    pi = quine_mccluskey(f)
    adj = build_graph(pi)
    tw = treewidth(adj)
    sigma_dnf_val = sigma_dnf(pi)
    
    return {
        "metric_name": "sigma_dnf",
        "metric_value": sigma_dnf_val,
        "instances_tested": 1,
        "conjecture_holds": sigma_dnf_val >= tw + 1,
        "counterexample": "" if sigma_dnf_val >= tw + 1 else f"f: {f}, pi: {pi}, sigma_dnf: {sigma_dnf_val}, tw: {tw}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    sigma_dnf_vals = [r["metric_value"] for r in results]
    tw_plus_1_vals = [tw + 1 for tw in treewidths(results)]
    
    mean_sigma_dnf = sum(sigma_dnf_vals) / len(sigma_dnf_vals)
    std_deviation = (sum((x - mean_sigma_dnf)**2 for x in sigma_dnf_vals) / len(sigma_dnf_vals))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_sigma_dnf} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")