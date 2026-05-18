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
        n = len(f[0])
        pi = set()
        for minterm in f:
            pi.add(tuple(minterm))
        
        # Simplify using Quine-McCluskey algorithm
        while True:
            new_pi = set()
            for p1, p2 in itertools.combinations(pi, 2):
                if sum(x != y for x, y in zip(p1, p2)) == 1:
                    new_p = tuple(sorted([i for i, (x, y) in enumerate(zip(p1, p2)) if x != y]))
                    new_pi.add(new_p)
            if len(new_pi) == len(pi):
                break
            pi = new_pi
        
        return list(pi)

    def is_compatible(p1, p2):
        for i in range(len(p1)):
            if (p1[i] == 0 and p2[i] == 1) or (p1[i] == 1 and p2[i] == 0):
                return False
        return True

    def treewidth(G):
        n = len(G)
        if n <= 2:
            return n - 1
        
        for u in range(n):
            neighbors = [v for v in range(n) if G[u][v]]
            if len(neighbors) == 0:
                continue
            w = neighbors[0]
            G[w] = [G[w][i] or (i != u and i != w) for i in range(n)]
            G[u] = [False] * n
            return max(treewidth(G), len(neighbors))
        
        return float('inf')

    def sigma_DNF(f):
        n = len(f[0])
        m = len(f)
        cover_matrix = [[False] * m for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                if all((f[i][k] == f[j][k]) or (f[i][k] == 2 and f[j][k] == 2) for k in range(n)):
                    cover_matrix[i][j] = True
                    cover_matrix[j][i] = True
        
        def branch_and_bound(cover, start=0):
            if start == m:
                return len(cover)
            
            min_cover_size = float('inf')
            for i in range(start, m):
                if not any(cover_matrix[i][j] and cover[j] for j in range(i)):
                    new_cover = cover[:]
                    new_cover[i] = True
                    min_cover_size = min(min_cover_size, branch_and_bound(new_cover, start + 1))
            return min_cover_size
        
        return branch_and_bound([False] * m)

    n = random.choice({6, 8, 10})
    k = 4
    terms = [tuple(random.sample(range(n), 3)) for _ in range(k)]
    f = [[2] * n for _ in range(1 << n)]
    for term in terms:
        for i in range(1 << n):
            m_bin = format(i, '0' + str(n) + 'b')
            if all((m_bin[j] == '1' and (i >> j) & 1) or (m_bin[j] == '0' and not ((i >> j) & 1)) for j in term):
                f[i] = [2 if x != y else y for x, y in zip(f[i], term)]
    
    pi = quine_mccluskey(f)
    G = [[is_compatible(p1, p2) for p2 in pi] for p1 in pi]
    tw = treewidth(G)
    sigma_dnf = sigma_DNF(pi)
    
    return {
        "metric_name": "sigma_DNF vs tw",
        "metric_value": sigma_dnf,
        "instances_tested": 1,
        "conjecture_holds": sigma_dnf >= tw + 1,
        "counterexample": "" if sigma_dnf >= tw + 1 else f"f: {f}, PI(f): {pi}, σ_DNF: {sigma_dnf}, tw(G(f)): {tw}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    sigma_dnf_values = [r["metric_value"] for r in results]
    tw_plus_one_values = [r["metric_value"] + 1 for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(sigma_dnf_values)/len(sigma_dnf_values):.2f} std={math.sqrt(sum((x - sum(sigma_dnf_values)/len(sigma_dnf_values))**2 for x in sigma_dnf_values) / len(sigma_dnf_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")