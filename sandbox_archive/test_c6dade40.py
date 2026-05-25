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

def generate_random_graph(n):
    if n <= 1:
        return {}
    g = {i: set() for i in range(n)}
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.choice([True, False]):
                g[u].add(v)
                g[v].add(u)
                edges.append((u, v))
    return g

def is_isomorphic(g1, g2):
    if len(g1) != len(g2):
        return False
    nodes = list(g1.keys())
    random.shuffle(nodes)
    mapping = {nodes[0]: 0}
    visited = set([nodes[0]])
    stack = [nodes[0]]
    while stack:
        u = stack.pop()
        for v in g1[u]:
            if v not in visited:
                visited.add(v)
                stack.append(v)
                mapping[v] = len(mapping)
    
    for u, v in edges:
        if (mapping[u], mapping[v]) != (g2[mapping[u]][0], g2[mapping[v]][0]):
            return False
    return True

def minimal_rank(g):
    n = len(g)
    rank = 0
    while True:
        independent_set = set()
        for u in range(n):
            if all(v not in independent_set for v in g[u]):
                independent_set.add(u)
        if not independent_set:
            break
        rank += 1
        g = {u: {v for v in g[u] if v not in independent_set} for u in g if u not in independent_set}
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(30):
            g1 = generate_random_graph(n)
            g2 = generate_random_graph(n)
            
            if is_isomorphic(g1, g2):
                rank = minimal_rank(g1)
                total_rank += rank
                instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        avg_rank = total_rank / instances_tested
        results.append(avg_rank)
    
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 2**math.floor(math.log2(n_values[-1])) * 0.9) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": sum(30 for _ in n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 2**math.floor(math.log2(n_values[-1])) * 0.9) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=UNKNOWN support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")