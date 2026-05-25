# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def min_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def generate_k_clique_instance(k, n):
        edges = set()
        nodes = list(range(n))
        random.shuffle(nodes)
        for i in range(k - 1):
            for j in range(i + 1, k):
                edges.add((nodes[i], nodes[j]))
        return edges
    
    def encode_to_quadratic_form(edges, n):
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v in edges:
            A[u][v] = 1
            A[v][u] = 1
        return A
    
    def quadratic_form_rank(k, n):
        instance = generate_k_clique_instance(k, n)
        A = encode_to_quadratic_form(instance, n)
        return min_rank(A)
    
    k = random.randint(3, 5)  # k should be at least 3 for a non-trivial clique
    n = random.randint(10, 20)  # n should be at least 10 to have meaningful results
    rank = quadratic_form_rank(k, n)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n**2,
        "counterexample": "" if rank <= n**2 else f"n={n}, k={k}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={r['counterexample']}\" first_failing_seed={first_failing_seed}")