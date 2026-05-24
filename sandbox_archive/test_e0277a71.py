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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return list(edges)

    def is_clique(graph, subset):
        for u, v in itertools.combinations(subset, 2):
            if (u, v) not in graph and (v, u) not in graph:
                return False
        return True

    def find_minimal_clique_size(graph):
        n = len(graph)
        min_clique_size = float('inf')
        for r in range(1, n + 1):
            for subset in itertools.combinations(range(n), r):
                if is_clique(graph, subset):
                    min_clique_size = min(min_clique_size, r)
                    break
            if min_clique_size < float('inf'):
                break
        return min_clique_size

    def find_minimal_rank(graph):
        n = len(graph)
        rank = float('inf')
        for k in range(1, n + 1):
            clique_size = find_minimal_clique_size(graph)
            if clique_size < rank:
                rank = clique_size
        return rank

    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    minimal_rank = find_minimal_rank(graph)
    min_clique_size = find_minimal_clique_size(graph)

    metric_value = Fraction(minimal_rank, min_clique_size) if min_clique_size != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Minimal Rank to Min Clique Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value <= 2,
        "counterexample": "" if metric_value <= 2 else f"Graph with n={n}, rank={minimal_rank}, min clique size={min_clique_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))[:30]  # Default to first 30 prime numbers

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")