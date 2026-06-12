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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def cyclic_cover(graph, n):
        # Simplified algorithm to find a cyclic cover
        cover = [set() for _ in range(n)]
        for u, v in graph:
            cover[u].add(v)
            cover[v].add(u)
        return cover
    
    def communication_complexity_rank_variance(cover, n):
        ranks = {}
        for i in range(n):
            rank = len(cover[i])
            if rank not in ranks:
                ranks[rank] = 0
            ranks[rank] += 1
        
        mean_rank = sum(rank * count for rank, count in ranks.items()) / n
        variance = sum(count * (rank - mean_rank) ** 2 for rank, count in ranks.items()) / n
        return variance
    
    def calculate_order(cover):
        # Simplified calculation of the order of the cyclic cover
        return len(set.union(*cover))
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    cover = cyclic_cover(graph, n)
    rank_variance = communication_complexity_rank_variance(cover, n)
    order = calculate_order(cover)
    
    if rank_variance == 0:
        return {
            "metric_name": "Order(G)",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "RankVar(G) is zero"
        }
    
    correlation_coefficient = order / rank_variance
    
    return {
        "metric_name": "Order(G)",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.5 and order <= 3 * rank_variance,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(res["metric_value"] for res in results) / len(results)
    std_order = math.sqrt(sum((res["metric_value"] - mean_order) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["metric_value"] < 3 * res["rank_variance"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order(G) < 3 * RankVar(G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")