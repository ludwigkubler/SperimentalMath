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
    if n < k:
        return None
    clique = [[0] * n for _ in range(n)]
    nodes = list(range(n))
    selected_nodes = random.sample(nodes, k)
    for u in selected_nodes:
        for v in selected_nodes:
            if u != v:
                clique[u][v] = 1
                clique[v][u] = 1
    return clique

def calculate_rank(clique):
    n = len(clique)
    rank = 0
    for i in range(n):
        if sum(clique[i]) > 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clique = generate_k_clique(n, random.randint(2, min(n - 1, 5)))
        if clique is None:
            continue
        rank = calculate_rank(clique)
        expected_rank = n * (n - 1) // 2
        if rank < expected_rank / 2 or rank > expected_rank * 2:
            return {
                "metric_name": "Rank vs DPLL Heig",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}"
            }
        results.append((n, rank))
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": sum(rank for _, rank in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(expected_rank / 2 <= rank <= expected_rank * 2 for n, rank in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(supported_count, len(results))
    mean_rank = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))

    if support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")