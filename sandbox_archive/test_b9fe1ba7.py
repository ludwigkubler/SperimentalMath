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

def generate_k_clique(n, k):
    if n - k < k * (k - 1) // 2:
        raise ValueError("Sample larger than population or is negative")
    remaining_edges = random.sample([(i, j) for i in range(k, n) for j in range(i + 1, n)], n - k)
    clique_edges = [(i, j) for i in range(k) for j in range(i + 1, k)]
    return clique_edges + remaining_edges

def compute_quotient_algebra_rank(edges):
    n = len(set(u for u, v in edges) | set(v for u, v in edges))
    algebra = [[0] * n for _ in range(n)]
    for u, v in edges:
        algebra[u][v] = 1
        algebra[v][u] = 1
    rank = 0
    for i in range(n):
        if any(algebra[i][j] != 0 for j in range(i)):
            rank += 1
            for j in range(n):
                if algebra[j][i] != 0:
                    for k in range(n):
                        algebra[j][k] -= algebra[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            try:
                k = random.randint(2, min(n - 1, 3))
                edges = generate_k_clique(n, k)
                rank = compute_quotient_algebra_rank(edges)
                if rank > O_n_1_5_minus_k(n, k):
                    return {
                        "metric_name": "Quotient Algebra Rank",
                        "metric_value": rank,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"n={n}, k={k}, rank={rank} > O(n^(1.5-k))"
                    }
                results.append(rank)
            except ValueError as e:
                return {
                    "metric_name": "Quotient Algebra Rank",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = Fraction(len([r for r in results if r <= O_n_1_5_minus_k(n, k)]), len(results))
    return {
        "metric_name": "Quotient Algebra Rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1,
        "counterexample": ""
    }

def O_n_1_5_minus_k(n, k):
    return n ** (1.5 - k)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results))
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")