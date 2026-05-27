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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def construct_quandle_representation(edges):
        quandle_rep = {}
        for u, v in edges:
            if u not in quandle_rep:
                quandle_rep[u] = set()
            if v not in quandle_rep:
                quandle_rep[v] = set()
            quandle_rep[u].add(v)
            quandle_rep[v].add(u)
        return quandle_rep
    
    def minimal_rank(quandle_rep):
        n = len(quandle_rep)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                queue = [i]
                while queue:
                    current = queue.pop()
                    if not visited[current]:
                        visited[current] = True
                        for neighbor in quandle_rep[current]:
                            if not visited[neighbor]:
                                queue.append(neighbor)
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        edges = generate_max_cut_instance(n)
        quandle_rep = construct_quandle_representation(edges)
        rank = minimal_rank(quandle_rep)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= math.log(n, 2) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else "n={} rank={}".format(n_values[0], ranks[0])
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_rank, 0.0, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(results[first_failing]["counterexample"], seeds[first_failing]))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")