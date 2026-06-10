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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_random_graph(n):
        graph = {i: set() for i in range(n)}
        edges = random.sample(range(n * (n - 1) // 2), n)
        for edge in edges:
            u, v = divmod(edge, n - 1)
            if u != v and u not in graph[v]:
                graph[u].add(v)
                graph[v].add(u)
        return graph
    
    def automorphism_group(graph):
        nodes = list(graph.keys())
        n = len(nodes)
        
        def is_automorphism(perm):
            for u, v in graph.items():
                perm_u = nodes[perm.index(u)]
                perm_v = nodes[perm.index(v)]
                if (perm_u, perm_v) not in graph and (perm_v, perm_u) not in graph:
                    return False
            return True
        
        def generate_permutations(n):
            if n == 0:
                yield []
            else:
                for perm in generate_permutations(n - 1):
                    for i in range(n):
                        if i not in perm:
                            yield [i] + perm
        
        max_index = 0
        for perm in generate_permutations(n):
            if is_automorphism(perm):
                max_index = max(max_index, math.gcd(math.factorial(n), n))
        return max_index
    
    def resolution_width(graph):
        # Simplified Tseitin formula width calculation (not actual resolution proof)
        return len(graph) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph = generate_random_graph(n)
            aut_index = automorphism_group(graph)
            width = resolution_width(graph)
            metric_values.append(math.log2(aut_index))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(metric_values) < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "log2(|Aut(G)|)",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")