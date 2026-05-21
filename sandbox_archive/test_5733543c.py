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
    
    def generate_monotone_dnf(n, m, k):
        terms = []
        for _ in range(m):
            term = set()
            while len(term) < k:
                u, v = random.sample(range(n), 2)
                if (u, v) not in term and (v, u) not in term:
                    term.add((u, v))
            terms.append(term)
        return terms
    
    def matching_polynomial(G, z):
        n1, n2 = len(G[0]), len(G[1])
        M = [[0] * (n1 + n2 + 1) for _ in range(n1 + n2 + 1)]
        M[n1][n2] = 1
        for u in G[0]:
            for v in G[1]:
                if (u, v) not in G:
                    continue
                M[u][v] += z * M[u-1][v-1]
                for w in range(v):
                    M[w][v] -= M[w][v-1]
        return [M[i][n2] for i in range(n1 + 1)]
    
    def sturm_sequence(poly):
        n = len(poly)
        s = [poly[:]]
        while True:
            if not s[-1]:
                break
            q = []
            r = s[-1]
            while len(r) > 0 and r[-1] != 0:
                d = r[-1]
                q.append([c / d for c in r[:-1]])
                r = [s[-2][-i-1] - (q[-1][-i-1] * s[-1][-i]) for i in range(len(s[-2])-len(q[-1]))]
            s.append(r)
        return s
    
    def min_root(poly):
        s = sturm_sequence(poly)
        signs = [(-1) ** i * poly[0] for i in range(len(s))]
        sign_changes = sum(signs[i] != signs[i+1] for i in range(len(signs)-1))
        if sign_changes == 0:
            return float('inf')
        else:
            return math.sqrt(2 * (sign_changes - 1))
    
    def mu(F):
        G = ([], [])
        for term in F:
            for edge in term:
                G[0].append(term)
                G[1].append(edge)
        poly = matching_polynomial(G, 1)
        rho = min_root(poly)
        return math.log2(1 + rho**2)
    
    n_values = [8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    for n in n_values:
        m = math.ceil(n ** 1.2)
        k_values = [2, 3, 4]
        
        random_dnf = generate_monotone_dnf(n, m, random.choice(k_values))
        random_mu = mu(random_dnf)
        results.append({
            "n": n,
            "m": m,
            "k": random.choice(k_values),
            "type": "random",
            "mu": random_mu
        })
        
        if n <= 14:
            clique_family_dnf = generate_monotone_dnf(n, math.comb(n, int(math.log2(n))), int(math.log2(n)))
        else:
            subgraph_size = n // 2
            subgraph_edges = [e for e in range(subgraph_size * (subgraph_size - 1) // 2)]
            clique_family_dnf = generate_monotone_dnf(subgraph_size, math.comb(subgraph_size, int(math.log2(n))), int(math.log2(n)))
        clique_family_mu = mu(clique_family_dnf)
        results.append({
            "n": n,
            "m": math.comb(n, int(math.log2(n))),
            "k": int(math.log2(n)),
            "type": "clique-family",
            "mu": clique_family_mu
        })
    
    random_support = sum(1 for r in results if r["type"] == "random" and r["mu"] <= 1.5 * math.log2(r["n"])) >= 28
    clique_family_support = sum(1 for r in results if r["type"] == "clique-family" and r["mu"] >= 0.5 * math.sqrt(r["n"])) >= 28
    
    support_fraction = (random_support + clique_family_support) / len(results)
    
    if not random_support or not clique_family_support:
        return {
            "metric_name": "mu",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "support_condition_violated"
        }
    
    mean_mu = sum(r["mu"] for r in results) / len(results)
    std_mu = math.sqrt(sum((r["mu"] - mean_mu)**2 for r in results) / len(results))
    
    return {
        "metric_name": "mu",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    std_mu = math.sqrt(sum((r["metric_value"] - mean_mu)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_condition_violated' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_condition_violated")