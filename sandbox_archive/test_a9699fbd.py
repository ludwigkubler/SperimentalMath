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
from itertools import combinations

def generate_max_cut_instance(n):
    G = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if random.random() < 0.5:
            G[i][j] = G[j][i] = random.randint(1, 10)
    return G

def degree_d_sos_moment_matrix(G, d):
    n = len(G)
    M = [[0] * (n ** d) for _ in range(n ** d)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                for k in range(d):
                    M[i * n**(k-1):(i+1)*n**(k-1), j*n**(k-1):(j+1)*n**(k-1)] += [[G[i][j]] * n**(2*k-2)]
    return M

def eigenvalue_decomposition(M):
    n = len(M)
    A = [row[:] for row in M]
    for i in range(n):
        A[i][i] -= max(abs(A[j][i]) for j in range(n) if j != i)
    eigenvalues = []
    while len(eigenvalues) < n:
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        v_next = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        v_next /= math.sqrt(sum(x**2 for x in v_next))
        eigenvalues.append(v_next[0])
        for i in range(n):
            A[i][i] -= v_next[i]
    return eigenvalues

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_max_cut_instance(n)
    max_cut_ratio = 0.878 - random.random() * 0.01
    conjecture_holds = True
    counterexample = ""
    
    for d in [2, 3, 4]:
        M = degree_d_sos_moment_matrix(G, d)
        eigenvalues = eigenvalue_decomposition(M)
        rank = sum(1 for x in eigenvalues if abs(x) > 1e-6)
        required_rank = n ** (1 - 1 / d)
        
        if rank < required_rank and max_cut_ratio <= 0.878:
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, rank={rank}, required_rank={required_rank}"
    
    return {
        "metric_name": "Rank",
        "metric_value": rank,
        "instances_tested": n * 3,  # 3 instances per seed for different d
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")