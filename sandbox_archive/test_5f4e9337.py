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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def quine_mccluskey(f):
        n = len(next(iter(f.keys())))
        minterms = sorted(list(f.keys()))
        prime_implicants = []
        
        while True:
            new_pi = set()
            for i in range(len(minterms)):
                for j in range(i + 1, len(minterms)):
                    if all((m & (m ^ minterms[i]) == 0) and (m & (m ^ minterms[j]) == 0) for m in minterms):
                        new_pi.add(tuple(sorted(set(minterms[i] | minterms[j]))))
            if not new_pi:
                break
            prime_implicants.extend(new_pi)
            minterms = [m for m in minterms if any((m & (m ^ p) != 0) for p in prime_implicants)]
        
        return prime_implicants
    
    def is_compatible(p, q):
        for var in range(n):
            if p[var] != q[var] and p[var] != 2 and q[var] != 2:
                return False
        return True
    
    def build_graph(PI):
        n = len(PI)
        adj = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if is_compatible(PI[i], PI[j]):
                    adj[i][j] = 1
                    adj[j][i] = 1
        return adj
    
    def treewidth(G):
        n = len(G)
        
        def dfs(node, parent, path):
            path.append(node)
            max_width = len(path) - 1
            for neighbor in range(n):
                if G[node][neighbor] and neighbor != parent:
                    width = dfs(neighbor, node, path)
                    if width > max_width:
                        max_width = width
            path.pop()
            return max_width
        
        return max(dfs(i, -1, []) for i in range(n))
    
    def sigma_DNF(f):
        n = len(next(iter(f.keys())))
        minterms = list(f.keys())
        pi_count = len(quine_mccluskey(f))
        
        cover_matrix = [[0] * (pi_count + 1) for _ in range(len(minterms))]
        for i, m in enumerate(minterms):
            for j, p in enumerate(quine_mccluskey(f)):
                if any((m & (m ^ p)) == 0 for p in quine_mccluskey(f)):
                    cover_matrix[i][j] = 1
        
        def branch_and_bound(matrix, pi_count):
            n = len(matrix)
            best_cover = pi_count + 1
            
            def backtrack(row, current_cover):
                nonlocal best_cover
                if row == n:
                    if current_cover < best_cover:
                        best_cover = current_cover
                    return
                for col in range(pi_count):
                    if matrix[row][col] == 0:
                        continue
                    new_cover = current_cover + (1 - matrix[row][col])
                    backtrack(row + 1, new_cover)
            
            backtrack(0, pi_count)
            return best_cover
        
        return branch_and_bound(cover_matrix, pi_count)
    
    n_values = [6, 8, 10]
    results = []
    
    for n in n_values:
        for _ in range(30):
            terms = []
            for _ in range(4):
                term = tuple(random.sample(range(n), 3))
                terms.append(term)
            
            f = {}
            for m in range(2**n):
                m_bin = format(m, '0{}b'.format(n))
                value = all(any((m_bin[i] == '1' and t[i] != 2) or (m_bin[i] == '0' and t[i] == 2) for i, t in enumerate(terms)) for term in terms)
                f[tuple(m_bin)] = int(value)
            
            PI = quine_mccluskey(f)
            G = build_graph(PI)
            tw = treewidth(G)
            sigma_dnf = sigma_DNF(f)
            
            if sigma_dnf < tw + 1:
                return {
                    "metric_name": "sigma_DNF vs tw",
                    "metric_value": sigma_dnf,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, PI={PI}, sigma_DNF={sigma_dnf}, tw={tw}"
                }
    
    return {
        "metric_name": "sigma_DNF vs tw",
        "metric_value": sum(sigma_DNF(f) for _ in range(30)) / 90,
        "instances_tested": 90,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 83))  # First 30 primes
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= max(results)) / len(results)
    
    if all(r >= max(results) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < max(results) for r in results):
        first_failing = next(i for i, r in enumerate(results) if r < max(results))
        print(f"RESULT: FALSIFIED counterexample='n=10' first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE reason=no_valid_data")