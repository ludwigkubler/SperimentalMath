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
from itertools import combinations, chain

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def powerset(s):
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    
    def mobius_function(lattice):
        n = len(lattice)
        mu = [[0] * n for _ in range(n)]
        mu[0][0] = 1
        for i in range(1, n):
            for j in range(i-1, -1, -1):
                if lattice[j].issubset(lattice[i]):
                    mu[i][j] = -mu[i-1][j]
                    break
            for j in range(i+1, n):
                if lattice[j].issubset(lattice[i]):
                    mu[i][j] = mu[i-1][j]
        return mu
    
    def zeta_inversion(mu):
        n = len(mu)
        zeta = [[0] * n for _ in range(n)]
        for i in range(n):
            zeta[0][i] = 1
            for j in range(1, i+1):
                zeta[j][i] = sum(zeta[k][i-1] * mu[i-j+k][k] for k in range(j))
        return zeta
    
    def log2(x):
        return math.log2(x)
    
    def triangle_dnf(n):
        edges = list(combinations(range(n), 2))
        minterms = []
        for edge_set in combinations(edges, n-3):
            minterm = set()
            for edge in edge_set:
                minterm.update(edge)
            minterms.append(minterm)
        return minterms
    
    def random_monotone_dnf(n, s, min_minterm_size=2, max_minterm_size=5):
        minterms = []
        while len(minterms) < s:
            minterm_size = random.randint(min_minterm_size, max_minterm_size)
            minterm = set(random.sample(range(n), minterm_size))
            if all(not m.issubset(minterm) for m in minterms):
                minterms.append(minterm)
        return minterms
    
    def compute_lambda(lattice):
        mu = mobius_function(lattice)
        zeta = zeta_inversion(mu)
        return sum(abs(zeta[i][0]) for i in range(1, len(lattice)))
    
    n_graphs = [4, 5, 6, 7]
    k = 3
    max_random_lambda = 0
    
    for n_graph in n_graphs:
        n = math.comb(n_graph, 2)
        triangle_minterms = triangle_dnf(n_graph)
        L_triangle = powerset(triangle_minterms)
        mu_triangle = mobius_function(L_triangle)
        zeta_triangle = zeta_inversion(mu_triangle)
        lambda_triangle = sum(abs(zeta_triangle[i][0]) for i in range(1, len(L_triangle)))
        
        if lambda_triangle > max_random_lambda:
            max_random_lambda = lambda_triangle
        
        for s in [n, 2*n, 4*n, 8*n]:
            random_minterms = random_monotone_dnf(n, s)
            L_random = powerset(random_minterms)
            mu_random = mobius_function(L_random)
            zeta_random = zeta_inversion(mu_random)
            lambda_random = sum(abs(zeta_random[i][0]) for i in range(1, len(L_random)))
            
            if lambda_random > max_random_lambda:
                max_random_lambda = lambda_random
    
    conjecture_holds = (lambda_triangle >= (1/8) * n_graphs[0] * log2(n_graphs[0])) and \
                       all(lambda_random <= 4 * log2(s+1) * log2(n+1) for s in [n, 2*n, 4*n, 8*n])
    
    return {
        "metric_name": "Lambda",
        "metric_value": lambda_triangle,
        "instances_tested": len(n_graphs),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Triangle-DNF: Lambda(F)={lambda_triangle}, max_random_lambda={max_random_lambda}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lambda = sum(r["metric_value"] for r in results) / len(results)
    std_lambda = math.sqrt(sum((r["metric_value"] - mean_lambda) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lambda} std={std_lambda} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"Lambda(F_triangle)<(1/8)*n*log2(n)\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")