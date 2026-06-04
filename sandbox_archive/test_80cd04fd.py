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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges = set()
        nodes = list(range(n))
        
        while len(edges) < (n * d) // 2:
            node1, node2 = random.sample(nodes, 2)
            if (node1, node2) not in edges and (node2, node1) not in edges:
                graph[node1].append(node2)
                graph[node2].append(node1)
                edges.add((node1, node2))
        
        return graph
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            rank += len(graph[i])
        return rank
    
    def minimal_symplectic_volume(graph):
        n = len(graph)
        vol_m_G = 0
        for node in graph:
            for neighbor in graph[node]:
                if (node, neighbor) not in edges and (neighbor, node) not in edges:
                    edges.add((node, neighbor))
                    vol_m_G += 1
        return vol_m_G
    
    a = Fraction(1, 2)
    d = random.randint(3, 5)
    
    results = []
    for n in range(5, 41):
        graph = generate_d_regular_graph(n, d)
        vol_m_G = minimal_symplectic_volume(graph)
        r_G = communication_complexity_rank(graph)
        
        if r_G == 0:
            continue
        
        ratio = Fraction(vol_m_G, r_G)
        results.append(ratio)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(ratio >= a * math.log(d, 2) for ratio in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "vol_m(G)/r(G)",
        "metric_value": float(metric_value),
        "instances_tested": len(results),
        "n_max": max(range(5, 41)),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    support_fraction = sum(result >= a * math.log(d, 2) for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={math.sqrt(sum((x - mean)**2 for x in results) / len(results)):.4f} support_fraction={support_fraction:.2f}")
    elif any(result < a * math.log(d, 2) for result in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")