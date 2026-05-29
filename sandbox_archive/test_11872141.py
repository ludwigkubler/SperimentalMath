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
    
    def generate_dnf(N, k):
        return set(random.sample(range(1, N+1), k) for _ in range(20))
    
    def reduce_dnf(dnf):
        dnf = list(dnf)
        n = len(dnf)
        while True:
            changed = False
            for i in range(n-1):
                for j in range(i+1, n):
                    if dnf[i].issubset(dnf[j]):
                        del dnf[j]
                        n -= 1
                        changed = True
                    elif dnf[j].issubset(dnf[i]):
                        del dnf[i]
                        n -= 1
                        changed = True
            if not changed:
                break
        return set(dnf)
    
    def compute_overlap_graph(dnf):
        terms = list(dnf)
        n = len(terms)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if terms[i].intersection(terms[j]):
                    A[i][j] = 1
                    A[j][i] = 1
        return A
    
    def compute_forman_ricci_curvature(A):
        n = len(A)
        deg = [sum(row) for row in A]
        tri = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if A[i][j]:
                    for k in range(j+1, n):
                        if A[i][k] and A[j][k]:
                            tri[i][j] += 1
        mu = sum(4 - deg[i] - deg[j] + 3 * tri[i][j] for i in range(n) for j in range(i+1, n)) / (n * (n-1))
        return mu
    
    def compute_lattice_submodularity_defect(F, G):
        F_and_G = reduce_dnf(F.union(G))
        F_or_G = reduce_dnf(F.intersection(G))
        mu_F_and_G = compute_forman_ricci_curvature(compute_overlap_graph(F_and_G))
        mu_F_or_G = compute_forman_ricci_curvature(compute_overlap_graph(F_or_G))
        mu_F = compute_forman_ricci_curvature(compute_overlap_graph(F))
        mu_G = compute_forman_ricci_curvature(compute_overlap_graph(G))
        return abs(mu_F_and_G + mu_F_or_G - mu_F - mu_G)
    
    N = 40
    k = math.ceil(math.log2(N))
    F = reduce_dnf(generate_dnf(N, k))
    G = reduce_dnf(generate_dnf(N, k))
    
    delta = compute_lattice_submodularity_defect(F, G)
    
    return {
        "metric_name": "lattice_submodularity_defect",
        "metric_value": delta,
        "instances_tested": 1,
        "n_max": N,
        "conjecture_holds": delta <= 4 * math.sqrt(N),
        "counterexample": "" if delta <= 4 * math.sqrt(N) else f"delta={delta} > 4*sqrt({N})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_delta = sum(r["metric_value"] for r in results) / len(results)
    std_delta = math.sqrt(sum((r["metric_value"] - mean_delta)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_delta} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"delta exceeded 4*sqrt(N)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")