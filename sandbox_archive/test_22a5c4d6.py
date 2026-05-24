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

def generate_k_clique(n, k):
    if n < k:
        raise ValueError("n must be greater than or equal to k")
    nodes = list(range(n))
    clique = random.sample(nodes, k)
    for i in range(k):
        for j in range(i + 1, k):
            clique[i][j] = 1
            clique[j][i] = 1
    return clique

def calculate_rank(clique):
    n = len(clique)
    rank = 0
    for i in range(n):
        for j in range(i + 1, n):
            if clique[i][j] == 1:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            try:
                clique = generate_k_clique(n, random.randint(2, min(n - 1, 5)))
                rank = calculate_rank(clique)
                expected_rank = n**2 * math.log(n)
                if rank < expected_rank / 2 or rank > expected_rank * 2:
                    return {
                        "metric_name": "Rank vs k-CLIQUE",
                        "metric_value": rank,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"n={n}, rank={rank} (expected: Θ({n**2 * math.log(n)}))"
                    }
            except ValueError as e:
                return {
                    "metric_name": "Rank vs k-CLIQUE",
                    "metric_value": None,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    return {
        "metric_name": "Rank vs k-CLIQUE",
        "metric_value": None,
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)

    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results) if results else 0
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")