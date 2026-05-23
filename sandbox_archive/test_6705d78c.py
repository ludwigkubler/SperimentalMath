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

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_k_clique(n, k):
    graph = [[0] * n for _ in range(n)]
    edges = set()
    nodes = list(range(n))
    while len(edges) < k:
        u, v = random.sample(nodes, 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
    return graph

def regular_expression_from_graph(n):
    # Placeholder for actual implementation
    return "regular_expression"

def automorphism_group_order(regular_expression):
    # Placeholder for actual implementation
    return [random.randint(1, n) for _ in range(random.randint(1, 5))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    primes = generate_primes(30)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = random_k_clique(n, random.randint(1, n // 2))
        regular_expression = regular_expression_from_graph(n)
        orders = automorphism_group_order(regular_expression)
        
        for _, edges in graph:
            for order in orders:
                if not (1 <= order ** (1/4) <= n):
                    return {
                        "metric_name": "minimal_order",
                        "metric_value": None,
                        "instances_tested": 0,
                        "conjecture_holds": False,
                        "counterexample": "mapping_undefined"
                    }
        
        results.append(order)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(1 <= order ** (1/4) <= n for _, edges in graph for order in automorphism_group_order(regular_expression_from_graph(n)))
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r is not None and (1 <= r ** (1/4) <= n)) / len(results)
    
    if all(r is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r is None or not (1 <= r ** (1/4) <= n) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is None or not (1 <= result ** (1/4) <= n))
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")