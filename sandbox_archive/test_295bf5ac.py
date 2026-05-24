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
    
    def generate_k_clique(n, k):
        if k > n or k == 0:
            return None
        nodes = list(range(1, n + 1))
        clique = set(random.sample(nodes, k))
        graph = {node: set() for node in nodes}
        for i in range(k):
            for j in range(i + 1, k):
                graph[nodes[i]].add(nodes[j])
                graph[nodes[j]].add(nodes[i])
        return graph

    def calculate_rank(graph):
        if not graph:
            return 0
        n = len(graph)
        rank = 0
        for node in graph:
            rank += len(graph[node])
        return rank / 2

    def k_clique_lower_bound(n, k):
        if k > n or k == 0:
            return None
        return math.comb(n, k)

    results = []
    for n in range(1, 41):
        for _ in range(3):  # Ensure at least 3 instances per size
            graph = generate_k_clique(n, random.randint(2, min(n - 1, 5)))
            if graph is None:
                continue
            rank = calculate_rank(graph)
            lower_bound = k_clique_lower_bound(n, random.randint(2, min(n - 1, 5)))
            if lower_bound is None:
                continue
            results.append({
                "n": n,
                "rank": rank,
                "lower_bound": lower_bound
            })

    if not results:
        return {
            "metric_name": "Rank vs k-CLIQUE Lower Bound",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }

    rank_values = [result["rank"] for result in results]
    lower_bound_values = [result["lower_bound"] for result in results]

    mean_rank = sum(rank_values) / len(rank_values)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in rank_values) / len(rank_values))
    mean_lower_bound = sum(lower_bound_values) / len(lower_bound_values)
    std_lower_bound = math.sqrt(sum((x - mean_lower_bound) ** 2 for x in lower_bound_values) / len(lower_bound_values))

    support_fraction = sum(1 for result in results if abs(result["rank"] - result["lower_bound"]) <= 2 * result["lower_bound"]) / len(results)

    return {
        "metric_name": "Rank vs k-CLIQUE Lower Bound",
        "metric_value": mean_rank,
        "instances_tested": len(rank_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, rank={results[0]['rank']}, lower_bound={results[0]['lower_bound']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, rank={results[0]['rank']}, lower_bound={results[0]['lower_bound']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")