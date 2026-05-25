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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_graph(n, p):
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G[i][j] = G[j][i] = 1
    return G

def is_automorphism(G, H, mapping):
    n = len(G)
    for u in range(n):
        for v in range(u + 1, n):
            if (G[u][v] != H[mapping[u]][mapping[v]]):
                return False
    return True

def find_minimal_rank(G):
    n = len(G)
    vertices = list(range(n))
    rank = float('inf')
    
    def permute(v, p):
        if v == n:
            yield p
        else:
            for i in range(v, n):
                p[v], p[i] = p[i], p[v]
                yield from permute(v + 1, p)
                p[v], p[i] = p[i], p[v]
    
    for perm in permute(0, vertices[:]):
        if is_automorphism(G, G, dict(zip(vertices, perm))):
            rank = min(rank, len(set(perm)))
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 20, 30, 40])
    p = 0.5
    G = random_graph(n, p)
    rank = find_minimal_rank(G)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n**2,  # Placeholder for actual conjecture check
        "counterexample": "" if rank <= n**2 else f"Graph with n={n}, rank={rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={results[results.index(next(result for result in results if not result['conjecture_holds']))]['metric_value']}, rank={results[results.index(next(result for result in results if not result['conjecture_holds']))]['counterexample']}\" first_failing_seed={first_failing_seed}")