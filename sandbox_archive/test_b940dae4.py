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
    def generate_read_twice_bp(n):
        bp = []
        for i in range(n):
            if random.choice([True, False]):
                bp.append((i, (i + 1) % n))
            else:
                bp.append(((i + 1) % n, i))
        return bp

    def state_transition_graph(bp):
        graph = {}
        for u, v in bp:
            if u not in graph:
                graph[u] = set()
            if v not in graph:
                graph[v] = set()
            graph[u].add(v)
            graph[v].add(u)
        return graph

    def persistent_homology(graph):
        # Simplified version of persistent homology using a filtration approach
        edges = []
        for u, neighbors in graph.items():
            for v in neighbors:
                if u < v:
                    edges.append((u, v))
        edges.sort(key=lambda x: len(set(x)))
        
        persistence = 0
        visited = set()
        for u, v in edges:
            if u not in visited and v not in visited:
                persistence += 1
                visited.add(u)
                visited.add(v)
        return persistence

    def is_ip2(bp):
        # Check if the BP computes IP_2
        n = len(bp)
        for i in range(n):
            if (i, (i + 1) % n) not in bp and ((i + 1) % n, i) not in bp:
                return False
        return True

    def random_function_bp(n):
        bp = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    bp.append((i, j))
                else:
                    bp.append((j, i))
        return bp

    random.seed(seed)
    
    n = random.randint(5, 40)
    bp_ip2 = generate_read_twice_bp(n)
    bp_random = random_function_bp(n)
    
    persistence_ip2 = persistent_homology(state_transition_graph(bp_ip2))
    persistence_random = persistent_homology(state_transition_graph(bp_random))
    
    metric_name = "persistence"
    metric_value_ip2 = persistence_ip2
    metric_value_random = persistence_random
    
    instances_tested = 2
    conjecture_holds_ip2 = persistence_ip2 >= n
    conjecture_holds_random = persistence_random <= math.log(len(bp_random))
    
    counterexample = ""
    if not conjecture_holds_ip2:
        counterexample += "IP_2 BP failed: persistence(P) < Ω(n)\n"
    if not conjecture_holds_random:
        counterexample += "Random function BP failed: persistence(P) > O(log size(P))"
    
    return {
        "metric_name": metric_name,
        "metric_value_ip2": metric_value_ip2,
        "metric_value_random": metric_value_random,
        "instances_tested": instances_tested,
        "conjecture_holds_ip2": conjecture_holds_ip2,
        "conjecture_holds_random": conjecture_holds_random,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 30))

    results_ip2 = []
    results_random = []

    for seed in seeds:
        result_ip2 = run_trial(seed)
        result_random = run_trial(seed)
        
        print(f"TRIAL: {result_ip2}")
        print(f"TRIAL: {result_random}")

        results_ip2.append(result_ip2["metric_value_ip2"])
        results_random.append(result_random["metric_value_random"])

    mean_ip2 = sum(results_ip2) / len(results_ip2)
    std_ip2 = math.sqrt(sum((x - mean_ip2) ** 2 for x in results_ip2) / len(results_ip2))
    support_fraction_ip2 = sum(1 for x in results_ip2 if x >= len(seeds)) / len(results_ip2)

    mean_random = sum(results_random) / len(results_random)
    std_random = math.sqrt(sum((x - mean_random) ** 2 for x in results_random) / len(results_random))
    support_fraction_random = sum(1 for x in results_random if x <= math.log(len(seeds))) / len(results_random)

    if support_fraction_ip2 >= 0.8 and support_fraction_random >= 0.8:
        print(f"RESULT: SUPPORTED mean_ip2={mean_ip2} std_ip2={std_ip2} support_fraction_ip2={support_fraction_ip2}")
        print(f"RESULT: SUPPORTED mean_random={mean_random} std_random={std_random} support_fraction_random={support_fraction_random}")
    elif any(x < len(seeds) for x in results_ip2):
        first_failing_seed = next(i for i, x in enumerate(results_ip2) if x < len(seeds))
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 BP failed\" first_failing_seed={first_failing_seed}")
    elif any(x > math.log(len(seeds)) for x in results_random):
        first_failing_seed = next(i for i, x in enumerate(results_random) if x > math.log(len(seeds)))
        print(f"RESULT: FALSIFIED counterexample=\"Random function BP failed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")