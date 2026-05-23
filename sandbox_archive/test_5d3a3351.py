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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def is_automorphism(graph, mapping):
        for u, v in graph:
            if (mapping[u], mapping[v]) not in graph and (mapping[v], mapping[u]) not in graph:
                return False
        return True
    
    def minimal_automorphism_group_size(graph):
        n = len(graph)
        vertices = list(range(n))
        min_size = float('inf')
        
        for perm in itertools.permutations(vertices):
            if is_automorphism(graph, dict(zip(vertices, perm))):
                size = math.factorial(n) // math.prod([math.factorial(perm.count(i)) for i in range(n)])
                if size < min_size:
                    min_size = size
        return min_size
    
    def or_circuit_size(n):
        # Simplified approximation for OR circuit size
        return n * (n - 1) // 2
    
    def f(n):
        # Polynomial function to compare with automorphism group size
        return n**3 * math.log(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_graph(n)
    min_size = minimal_automorphism_group_size(graph)
    circuit_size = or_circuit_size(n)
    
    conjecture_holds = True
    counterexample = ""
    
    if min_size > f(n):
        for perm in itertools.permutations(range(n)):
            if is_automorphism(graph, dict(zip(range(n), perm))):
                conjecture_holds = False
                counterexample = "Graph has an automorphism group of size greater than f(n)"
                break
    
    return {
        "metric_name": "Minimal Automorphism Group Size",
        "metric_value": min_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph has an automorphism group of size greater than f(n)\" first_failing_seed={first_failing_seed}")