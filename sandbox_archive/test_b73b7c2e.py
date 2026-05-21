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
    
    def generate_random_dnf(n, m, k):
        edges = list(itertools.combinations(range(n), 2))
        dnf = []
        for _ in range(m):
            term = random.sample(edges, k)
            dnf.append(term)
        return dnf
    
    def generate_clique_family_dnf(n, k):
        if n <= 14:
            cliques = list(itertools.combinations(range(n), k))
        else:
            subgraph_edges = random.sample(list(itertools.combinations(range(n // 2), 2)), k * (n // 2) // 2)
            subgraph_nodes = set().union(*subgraph_edges)
            cliques = [c for c in itertools.combinations(subgraph_nodes, k)]
        dnf = []
        for clique in cliques:
            term = [(i, j) for i, j in itertools.combinations(clique, 2)]
            dnf.append(term)
        return dnf
    
    def matching_polynomial(G, z):
        n = len(G)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        M[0][0] = 1
        for i in range(1, n + 1):
            for j in range(i):
                M[i][j] = M[i - 1][j]
            for u, v in G:
                if u < v:
                    M[v][u] = M[v - 1][u] * z - sum(M[u][w] for w in range(u + 1, v))
        return M[n][0]
    
    def sturm_sequence(poly):
        coeffs = poly[:]
        sturm = [coeffs]
        while True:
            if not sturm[-1]:
                break
            lead_coeff = sturm[-1][-1]
            next_poly = []
            for i in range(len(sturm[-1]) - 1, 0, -1):
                next_poly.append((sturm[-1][i] * (len(sturm[-1]) - i) / lead_coeff) - sturm[-2][i])
            sturm.append(next_poly)
        return sturm
    
    def min_root(poly):
        sturm = sturm_sequence(poly)
        signs = [(-1) ** len(coeffs) for coeffs in sturm]
        sign_changes = sum(signs[i] != signs[i + 1] for i in range(len(signs) - 1))
        return (2 ** ((sign_changes + 1) / 2)) if sign_changes > 0 else float('inf')
    
    def mu(F):
        G = {}
        for term, edges in enumerate(F):
            for edge in edges:
                if edge not in G:
                    G[edge] = set()
                G[edge].add(term)
        z = 1
        M_F = matching_polynomial(G, z)
        rho_F = min_root(M_F)
        return math.log2(1 + rho_F ** 2) if rho_F != float('inf') else float('inf')
    
    n_values = [8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40]
    results = []
    for n in n_values:
        m = math.ceil(n ** 1.2)
        k_values = [2, 3, 4]
        random_dnf_results = []
        clique_family_results = []
        
        for _ in range(30):
            dnf = generate_random_dnf(n, m, random.choice(k_values))
            mu_F = mu(dnf)
            random_dnf_results.append(mu_F)
            
            if n <= 14:
                dnf = generate_clique_family_dnf(n, math.floor(math.log2(n)))
            else:
                dnf = generate_clique_family_dnf(n // 2, math.floor(math.log2(n)) // 2)
            mu_F = mu(dnf)
            clique_family_results.append(mu_F)
        
        random_avg = sum(random_dnf_results) / len(random_dnf_results)
        clique_family_avg = sum(clique_family_results) / len(clique_family_results)
        results.append({
            "n": n,
            "random_avg": random_avg,
            "clique_family_avg": clique_family_avg
        })
    
    return {
        "metric_name": "mu",
        "metric_value": None,  # Not computed for this trial
        "instances_tested": len(n_values) * 30,
        "conjecture_holds": all(result["random_avg"] <= 1.5 * math.log2(n) and result["clique_family_avg"] >= 0.5 * math.sqrt(n) for n, _, _ in results),
        "counterexample": "" if all(result["random_avg"] <= 1.5 * math.log2(n) and result["clique_family_avg"] >= 0.5 * math.sqrt(n) for n, _, _ in results) else "n=8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    total_random_avg = sum(r["random_avg"] * r["instances_tested"] for r in all_results) / sum(r["instances_tested"] for r in all_results)
    total_clique_family_avg = sum(r["clique_family_avg"] * r["instances_tested"] for r in all_results) / sum(r["instances_tested"] for r in all_results)
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_random_avg} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=support_fraction_too_low")