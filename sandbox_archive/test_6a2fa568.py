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
    
    def generate_max_cut_instance(n):
        vertices = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(edges)
        cut_edges = edges[:n - 1]
        return vertices, cut_edges
    
    def tropicalized_quandle_representation(instance):
        vertices, cut_edges = instance
        quandle_rep = {}
        for v in vertices:
            quandle_rep[v] = set()
        for u, v in cut_edges:
            quandle_rep[u].add(v)
            quandle_rep[v].add(u)
        return quandle_rep
    
    def minimal_rank(quandle_rep):
        n = len(quandle_rep)
        rank = 0
        while True:
            found = False
            for i in range(n):
                if not quandle_rep[i]:
                    continue
                found = True
                for j in quandle_rep[i]:
                    quandle_rep[j].remove(i)
                del quandle_rep[i]
                break
            if not found:
                break
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        instance = generate_max_cut_instance(n)
        quandle_rep = tropicalized_quandle_representation(instance)
        rank = minimal_rank(quandle_rep)
        ranks.append(rank)
    
    metric_name = "min_rank"
    metric_value = sum(ranks) / len(ranks)
    instances_tested = len(ranks)
    conjecture_holds = all(rank <= math.log(n, 2) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else f"First failing instance with n={n_values[-1]}, rank={ranks[-1]}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing instance with n=40, rank={results[-1]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")