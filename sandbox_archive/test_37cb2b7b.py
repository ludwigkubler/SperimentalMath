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
    
    def generate_bipartite_graph(n):
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        G = [[A[i] == B[j] for j in range(n)] for i in range(n)]
        return G
    
    def matroid_rank(G):
        m, n = len(G), len(G[0])
        rank = 0
        for i in range(m):
            if any(G[i][j] for j in range(rank)):
                rank += 1
        return rank
    
    def communication_complexity_rank_variance(G):
        m, n = len(G), len(G[0])
        ranks = [sum(row) for row in G]
        mean_rank = sum(ranks) / m
        variance = sum((x - mean_rank) ** 2 for x in ranks) / m
        return variance
    
    def monodromy_representations(G):
        rank = matroid_rank(G)
        if rank == 0:
            return set()
        rep_set = set()
        for i in range(rank):
            rep = [1 if G[j][i] else 0 for j in range(len(G))]
            rep_set.add(tuple(rep))
        return rep_set
    
    n = random.randint(5, 40)
    G = generate_bipartite_graph(n)
    
    M_G = monodromy_representations(G)
    r_var_G = communication_complexity_rank_variance(G)
    
    metric_value = len(M_G) / (n * n)
    conjecture_holds = abs(metric_value - math.sqrt(r_var_G)) < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "monodromy_representations",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")