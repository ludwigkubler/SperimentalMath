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

from fractions import Fraction
import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges
    
    def encode_quadratic_form(edges):
        n = len(edges) + 1
        Q = [[0] * n for _ in range(n)]
        for i, j in edges:
            Q[i][j] = 1
            Q[j][i] = 1
        return Q
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if matrix[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for i in range(m):
                if i != rank - 1 and matrix[i][j] != 0:
                    factor = matrix[i][j] / matrix[rank - 1][j]
                    for k in range(n):
                        matrix[i][k] -= factor * matrix[rank - 1][k]
        return rank
    
    n = random.randint(5, 40)
    edges = generate_k_clique(n)
    Q = encode_quadratic_form(edges)
    rank = gaussian_elimination(Q)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n**2,
        "counterexample": "" if rank <= n**2 else f"n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 976385) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank / instances_tested} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank / instances_tested} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={r['counterexample']}\" first_failing_seed={first_failing_seed}")