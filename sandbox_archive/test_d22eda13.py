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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return {u: [v for v in range(n) if (u, v) in edges or (v, u) in edges] for u in range(n)}
    
    def min_cyclic_cover(graph):
        n = len(graph)
        covered = [False] * n
        cover_count = 0
        
        while not all(covered):
            start_node = random.choice([i for i in range(n) if not covered[i]])
            stack = [start_node]
            while stack:
                node = stack.pop()
                if not covered[node]:
                    covered[node] = True
                    cover_count += 1
                    for neighbor in graph[node]:
                        if not covered[neighbor]:
                            stack.append(neighbor)
        return cover_count
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        ranks = []
        
        for partition_size in range(1, n):
            rank_sum = 0
            for _ in range(10):  # Sample multiple partitions to get a good average
                partition = random.sample(range(n), partition_size)
                rank = sum(len(graph[node]) for node in partition) / partition_size
                rank_sum += rank
            ranks.append(rank_sum / 10)
        
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((rank - mean_rank) ** 2 for rank in ranks) / len(ranks)
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    order_sum = 0
    rank_var_sum = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_random_graph(n)
        order = min_cyclic_cover(graph)
        rank_var = communication_complexity_rank_variance(graph)
        
        if order > 3 * rank_var:
            return {
                "metric_name": "Order(G)",
                "metric_value": order,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Order(G) > 3 * RankVar(G) for n={n}"
            }
        
        order_sum += order
        rank_var_sum += rank_var
        instances_tested += len(n_values)
    
    mean_order = order_sum / instances_tested
    mean_rank_var = rank_var_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * rank_var for order, rank_var in zip(order_sum, rank_var_sum)) -
                                order_sum * rank_var_sum) / math.sqrt(instances_tested * sum(order ** 2 for order in order_sum) - order_sum ** 2 *
                                                                 instances_tested * sum(rank_var ** 2 for rank_var in rank_var_sum) - rank_var_sum ** 2)
    
    return {
        "metric_name": "Order(G)",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5 and all(order <= 3 * rank_var for order, rank_var in zip(order_sum, rank_var_sum)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["order"] > 3 * r["rank_var"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order(G) > 3 * RankVar(G)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")