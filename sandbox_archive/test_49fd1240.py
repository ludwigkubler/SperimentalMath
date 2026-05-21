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
    
    def generate_random_dnf(n, m, k):
        terms = []
        for _ in range(m):
            term = set(random.sample(range(1, n+1), k))
            terms.append(term)
        return terms
    
    def generate_clique_dnf(n, k):
        edges = [(i, j) for i in range(1, n+1) for j in range(i+1, n+1)]
        clique_terms = []
        for edge in edges:
            if len(edge) == k:
                clique_terms.append(set(edge))
        return clique_terms
    
    def matching_polynomial(G, z):
        m = len(G)
        n = len(G[0])
        M = [[0] * (m + n + 1) for _ in range(m + n + 1)]
        M[m][n] = 1
        for i in range(m):
            for j in range(n):
                if G[i][j]:
                    M[i+1][j+1] += M[i][j]
                    M[i+n+1][j+1] -= M[i][j]
        return M
    
    def sturm_sequence(poly):
        n = len(poly)
        s = [poly[:]]
        while True:
            if not s[-1]:
                break
            q, r = divmod(s[-2], s[-1])
            s.append(r)
        return s
    
    def min_root(poly):
        sturm = sturm_sequence(poly)
        sign_changes = 0
        for i in range(1, len(sturm)):
            if sturm[i-1] * sturm[i] < 0:
                sign_changes += 1
        if sign_changes % 2 == 0:
            return -1
        else:
            low, high = -1, 1
            while high - low > 1e-10:
                mid = (low + high) / 2
                if poly(mid) * sturm[0](mid) < 0:
                    low = mid
                else:
                    high = mid
            return low
    
    def mu(dnf):
        G = [[0] * len(dnf) for _ in range(len(dnf))]
        for i, term in enumerate(dnf):
            for j in range(i+1, len(dnf)):
                if not term.isdisjoint(dnf[j]):
                    G[i][j] = 1
                    G[j][i] = 1
        M_F = matching_polynomial(G, z)
        rho_F = min_root(M_F)
        return math.log2(1 + rho_F**2) if rho_F != -1 else float('inf')
    
    def run_test(n):
        m = int(math.ceil(n ** 1.2))
        k_values = [2, 3, 4]
        random_dnf = generate_random_dnf(n, m, random.choice(k_values))
        clique_dnf = generate_clique_dnf(n, math.floor(math.log2(n)))
        
        mu_random = mu(random_dnf)
        mu_clique = mu(clique_dnf)
        
        return {
            "metric_name": "mu",
            "metric_value": (mu_random + mu_clique) / 2,
            "instances_tested": 2,
            "conjecture_holds": mu_random <= 1.5 * math.log2(n) and mu_clique >= 0.5 * math.sqrt(n),
            "counterexample": ""
        }
    
    seeds = [seed]
    results = []
    for s in seeds:
        result = run_test(s)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    run_trial(seeds[0])