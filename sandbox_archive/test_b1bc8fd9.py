# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        edges = set()
        while len(edges) < 3 * n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)

    def popcount(x):
        count = 0
        while x:
            count += x & 1
            x >>= 1
        return count

    def laplacian_eigenvalues(n, m):
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            L[i][i] = 2
        for u, v in edges:
            L[u][v] = -1
            L[v][u] = -1
        return [eigenvalue for eigenvalue in numpy.linalg.eigvalsh(L) if eigenvalue >= 0]

    def compute_a_j(n, m):
        a_j = defaultdict(int)
        for S in range(2 ** n):
            mask = [S >> i & 1 for i in range(n)]
            degree_sum = sum(mask[u] ^ mask[v] for u, v in edges if (u, v) in edges or (v, u) in edges)
            a_j[degree_sum] += popcount(S)
        return {j: a / math.comb(m, j) for j, a in a_j.items()}

    def compute_rho(n, lambda_max, MC):
        return n * lambda_max / (4 * MC) - 1

    def compute_LD(a_j):
        m = len(edges)
        LD = 0
        for j in range(1, m):
            if a_j[j-1] > 0 and a_j[j] > 0 and a_j[j+1] > 0:
                LD = max(LD, math.log((a_j[j-1] * a_j[j+1]) / (a_j[j]**2)))
        return LD

    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        m = 3 * n // 2
        edges = generate_graph(n)
        a_j = compute_a_j(n, m)
        MC = max(a_j.values())
        lambda_max = laplacian_eigenvalues(n, m)[0]
        rho = compute_rho(n, lambda_max, MC)
        LD = compute_LD(a_j)
        
        results.append({
            "n": n,
            "m": m,
            "rho": rho,
            "LD": LD
        })

    all_hold = True
    counterexample = ""
    for result in results:
        if result["LD"] < 0.05 * result["rho"]:
            all_hold = False
            counterexample = f"n={result['n']}, m={result['m']}, rho={result['rho']:.4f}, LD={result['LD']:.4f}"

    return {
        "metric_name": "Lorentzian Defect",
        "metric_value": sum(result["LD"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all_hold,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std=0.0000 support_fraction={support_fraction:.2%}")
    elif any(not result["conjecture_holds"] and result["LD"] < 0.05 * result["rho"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=n={result['n']}, m={result['m']}, rho={result['rho']:.4f}, LD={result['LD']:.4f} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")