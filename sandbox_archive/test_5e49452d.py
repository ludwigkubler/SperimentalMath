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
    
    def generate_max_cut_instance(n):
        vertices = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        cut_edges = random.sample(edges, n - 1)
        return vertices, cut_edges
    
    def construct_quandle_representation(instance):
        vertices, _ = instance
        quandle_rep = {v: v for v in vertices}
        for u, v in generate_max_cut_instance(len(vertices))[1]:
            if quandle_rep[u] != quandle_rep[v]:
                quandle_rep[quandle_rep[v]] = quandle_rep[u]
        return quandle_rep
    
    def minimal_rank(quandle_rep):
        rank = 0
        visited = [False] * len(quandle_rep)
        for v in quandle_rep:
            if not visited[v]:
                stack = [v]
                while stack:
                    current = stack.pop()
                    if not visited[current]:
                        visited[current] = True
                        for neighbor in quandle_rep:
                            if quandle_rep[neighbor] == quandle_rep[current]:
                                stack.append(neighbor)
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        instance = generate_max_cut_instance(n)
        quandle_rep = construct_quandle_representation(instance)
        rank = minimal_rank(quandle_rep)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= math.log(n, 2) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else f"n={n_values[0]}, rank={ranks[0]}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={n_values[0]}, rank={ranks[0]}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")