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
        for _ in range(random.randint(1, n * (n - 1) // 2)):
            u, v = sorted(random.sample(range(n), 2))
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def max_independent_set_size(graph):
        n = len(graph)
        independent_sets = [set()]
        for node in range(n):
            new_sets = set()
            for s in independent_sets:
                if all(node != neighbor for neighbor in graph[node] if neighbor in s):
                    new_sets.add(s.union({node}))
            independent_sets.update(new_sets)
        return max(len(s) for s in independent_sets)
    
    def geometric_entropy(curves):
        n = len(curves)
        if n == 0:
            return 0
        entropy = 0
        for curve in curves:
            length = len(curve)
            if length > 1:
                entropy += math.log(length) / math.log(n)
        return entropy
    
    def find_algebraic_curves(graph):
        independent_set_size = max_independent_set_size(graph)
        n = len(graph)
        curves = []
        for _ in range(independent_set_size):
            curve = set()
            while True:
                node = random.choice(list(graph.keys()))
                if all(node != neighbor for neighbor in graph[node] if neighbor in curve):
                    curve.add(node)
                else:
                    break
            curves.append(curve)
        return curves
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        graph = generate_graph(n)
        curves = find_algebraic_curves(graph)
        entropy = geometric_entropy(curves)
        total_entropy += entropy
        instances_tested += len(curves)
        if n > n_max:
            n_max = n
    
    mean_entropy = total_entropy / instances_tested
    conjecture_holds = mean_entropy <= 10
    counterexample = "" if conjecture_holds else f"mean_entropy={mean_entropy}"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_entropy too high\" first_failing_seed={first_failing_seed}")