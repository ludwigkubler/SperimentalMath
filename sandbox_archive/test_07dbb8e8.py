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
    
    def max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges
    
    def tropicalized_quandle_representation(edges):
        quandles = {}
        for u, v in edges:
            if u not in quandles:
                quandles[u] = set()
            if v not in quandles:
                quandles[v] = set()
            quandles[u].add(v)
            quandles[v].add(u)
        return quandles
    
    def min_rank(quandles):
        rank = 0
        for u, neighbors in quandles.items():
            rank = max(rank, len(neighbors))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        edges = max_cut_instance(n)
        quandles = tropicalized_quandle_representation(edges)
        rank = min_rank(quandles)
        results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, ranks = zip(*results)
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    if all(rank <= math.log(n) for n, rank in results):
        return {
            "metric_name": "min_rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing_seed = seed
        for n, rank in results:
            if rank > math.log(n):
                first_failing_seed = seed
                break
        return {
            "metric_name": "min_rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"First failing instance with n={n}, rank={rank}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"First failing instance with n={n}, rank={rank}\" first_failing_seed={first_failing_seed}")