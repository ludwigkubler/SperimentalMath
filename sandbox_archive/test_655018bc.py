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

def generate_random_graph(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.append((i, j))
    return edges

def is_clique(graph, subset):
    for u in subset:
        for v in subset:
            if (u, v) not in graph and (v, u) not in graph:
                return False
    return True

def find_max_clique(graph, n):
    max_clique = []
    for i in range(1 << n):
        subset = [j for j in range(n) if (i & (1 << j))]
        if is_clique(graph, subset) and len(subset) > len(max_clique):
            max_clique = subset
    return max_clique

def polymatroid_rank(graph, n):
    rank = 0
    for i in range(1 << n):
        subset = [j for j in range(n) if (i & (1 << j))]
        clique_size = len(find_max_clique(graph, n))
        rank = max(rank, clique_size)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    min_rank = float('inf')
    instances_tested = 30
    
    for _ in range(instances_tested):
        graph = generate_random_graph(n)
        rank = polymatroid_rank(graph, n)
        if rank < min_rank:
            min_rank = rank
    
    conjecture_holds = min_rank >= 6.4
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}"
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": min_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank={result['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")