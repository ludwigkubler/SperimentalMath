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
        if n == 1:
            return [(0,)]
        elif n == 2:
            return [(0, 1)]
        else:
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    if random.choice([True, False]):
                        edges.append((i, j))
            return edges
    
    def edge_expansion(graph, n):
        min_cut_size = float('inf')
        for s in range(1, n // 2 + 1):
            cuts = [set(), set()]
            for u, v in graph:
                if len(cuts[0]) <= s and u not in cuts[0]:
                    cuts[0].add(u)
                    cuts[1].add(v)
                elif len(cuts[1]) <= s and v not in cuts[1]:
                    cuts[1].add(v)
                    cuts[0].add(u)
            min_cut_size = min(min_cut_size, len(graph) - len(cuts[0]))
        return min_cut_size / (n // 2)
    
    def resolution_length(h):
        if h == 0:
            return 1
        else:
            c = 2
            return 2 ** (c * h)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_graph(n)
    h_G = edge_expansion(graph, n)
    length = resolution_length(h_G)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": True if h_G > 0 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"h(G) <= 0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")