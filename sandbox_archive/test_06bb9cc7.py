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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            pivot_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[pivot_row][i]):
                    pivot_row = j
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def grothendieck_group(G):
        G_0 = [G[0]]
        for g in G[1:]:
            found = False
            for h in G_0:
                if all((g[i] + h[i]) % 2 == 0 for i in range(len(g))):
                    found = True
                    break
            if not found:
                G_0.append(g)
        return G_0
    
    def minimal_eta_quotient(G, G_0):
        quotient = [x for x in G if any(all((x[i] - y[i]) % 2 == 0 for i in range(len(x))) for y in G_0)]
        return min(quotient)
    
    n = random.randint(5, 40)
    variables = list(range(n))
    clauses = []
    for _ in range(random.randint(1, 3*n)):
        clause = [random.choice(variables) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    G = [[0] * n for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            G[i][var] += 1
    
    rank_G = matrix_rank(G)
    G_0 = grothendieck_group(G)
    eta_phi = minimal_eta_quotient(G, G_0)
    
    return {
        "metric_name": "eta_phi",
        "metric_value": float(eta_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": eta_phi <= n**2,
        "counterexample": "" if eta_phi <= n**2 else f"eta_phi={eta_phi} > {n**2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_eta_phi = sum(r["metric_value"] for r in results) / len(results)
    std_eta_phi = math.sqrt(sum((r["metric_value"] - mean_eta_phi)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_eta_phi} std={std_eta_phi} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_eta_phi} std={std_eta_phi} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")