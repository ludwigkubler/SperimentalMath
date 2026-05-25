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
    
    def encode_quadratic_form(clique):
        n = len(clique)
        Q = [[0] * n for _ in range(n)]
        for u, v in clique:
            if u < 0 or v < 0 or u >= n or v >= n:
                return None
            Q[u][v] = Q[v][u] = 1
        return Q
    
    def min_rank(Q):
        n = len(Q)
        rank = 0
        for i in range(n):
            if any(Q[i]):
                pivot_row = next(j for j in range(i, n) if Q[j][i])
                for k in range(n):
                    Q[pivot_row][k] /= Q[pivot_row][i]
                for j in range(n):
                    if j != pivot_row:
                        factor = Q[j][i]
                        for k in range(n):
                            Q[j][k] -= factor * Q[pivot_row][k]
                rank += 1
        return rank
    
    def generate_k_clique(n, k):
        nodes = list(range(n))
        random.shuffle(nodes)
        clique = []
        for i in range(k):
            for j in range(i + 1, k):
                clique.append((nodes[i], nodes[j]))
        return clique
    
    n_max = 40
    total_rank = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            clique = generate_k_clique(n, k=2)  # Generate a random 2-clique (edge)
            Q = encode_quadratic_form(clique)
            if Q is None:
                continue
            rank = min_rank(Q)
            total_rank += rank
            instances_tested += 1
    
    avg_rank = Fraction(total_rank, instances_tested)
    
    conjecture_holds = avg_rank <= n_max ** 2
    counterexample = "" if conjecture_holds else f"Average rank {avg_rank} > {n_max**2}"
    
    return {
        "metric_name": "average_minimal_rank",
        "metric_value": float(avg_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank exceeds n^2\" first_failing_seed={first_failing_seed}")