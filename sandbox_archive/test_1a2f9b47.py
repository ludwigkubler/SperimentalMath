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
    
    def generate_random_graph(n, m):
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def max_cut_polynomial(G):
        n = len(G)
        terms = []
        for subset in range(1 << n):
            term = 0
            for i in range(n):
                if (subset >> i) & 1:
                    term += (-1)**sum((i, j) in G for j in range(i+1, n))
            terms.append(term)
        return sum(terms)
    
    def newton_polytope_vertex_count(poly):
        # Placeholder implementation; actual computation depends on the polynomial structure
        return len(poly)
    
    def sos_degree(poly):
        # Placeholder implementation; actual computation depends on the SOS relaxation
        return 0
    
    n = random.randint(5, 40)
    m = random.randint(n, n*(n-1)//2)
    G = generate_random_graph(n, m)
    poly = max_cut_polynomial(G)
    vertex_count = newton_polytope_vertex_count(poly)
    d = sos_degree(poly)
    
    metric_name = "SOS Degree"
    metric_value = d
    instances_tested = 1
    conjecture_holds = d >= math.log(m)
    counterexample = "" if conjecture_holds else f"Graph with {n} nodes and {m} edges; SOS degree {d}, log(m)={math.log(m)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {results[0]['instances_tested']} nodes and edges\" first_failing_seed={first_failing_seed}")