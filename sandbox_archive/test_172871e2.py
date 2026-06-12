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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def cyclic_cover(graph, n):
        # Placeholder for the actual cyclic cover algorithm
        # This is a dummy implementation that returns a simple structure
        return [set(range(n))]
    
    def communication_complexity_rank_variance(graph, n):
        # Placeholder for the actual communication complexity rank variance calculation
        # This is a dummy implementation that returns a random value
        return random.random()
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_graph(n)
        cover = cyclic_cover(graph, n)
        rank_var = communication_complexity_rank_variance(graph, n)
        
        if len(cover) == 0:
            continue
        
        order = len(cover)
        results.append({
            "n": n,
            "order": order,
            "rank_var": rank_var
        })
    
    if not results:
        return {
            "metric_name": "Order(G)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "No valid cyclic cover found"
        }
    
    order_values = [r["order"] for r in results]
    rank_var_values = [r["rank_var"] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_rank_var = sum(rank_var_values) / len(rank_var_values)
    
    correlation_coefficient = 0
    if len(order_values) > 1:
        numerator = sum((order_values[i] - mean_order) * (rank_var_values[i] - mean_rank_var) for i in range(len(order_values)))
        denominator = math.sqrt(sum((order_values[i] - mean_order) ** 2 for i in range(len(order_values)))) * math.sqrt(sum((rank_var_values[i] - mean_rank_var) ** 2 for i in range(len(rank_var_values))))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = all(0.3 <= correlation_coefficient >= 0.5 and order <= 3 * rank_var for order, rank_var in zip(order_values, rank_var_values))
    
    return {
        "metric_name": "Order(G)",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Order(G) > 3 * RankVar(G) for n={max(r['n'] for r in results)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["order"] > 3 * r["rank_var"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Order(G) > 3 * RankVar(G)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")