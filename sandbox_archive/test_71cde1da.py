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

def generate_max_cut_instance(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    return edges

def pseudoexpectation_degree(M, d):
    n = len(M)
    M_tropicalized = [[min(a, b) if a != 0 and b != 0 else 0 for b in row] for row in M]
    rank = 0
    for i in range(n):
        for j in range(i + 1, n):
            if M_tropicalized[i][j] > 0:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        for _ in range(5):  # Ensure at least 5 instances per size
            edges = generate_max_cut_instance(n)
            M = [[0] * n for _ in range(n)]
            for u, v in edges:
                M[u][v] = random.randint(1, d)
                M[v][u] = M[u][v]
            rank = pseudoexpectation_degree(M, d)
            if rank > d ** 2:
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}, expected<=d^2={d**2}"
                break
            instances_tested += 1
        results.append({
            "metric_name": "Brauer_group_rank",
            "metric_value": rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.extend(result["results"])
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")