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

    def generate_bp(n):
        bp = []
        for i in range(n):
            if random.choice([True, False]):
                bp.append((i, (i + 1) % n))
        return bp

    def state_transition_graph(bp):
        graph = {}
        for u, v in bp:
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append(v)
            graph[v].append(u)
        return graph

    def persistent_homology(graph):
        # Simplified version of persistent homology using a filtration approach
        nodes = list(graph.keys())
        edges = set()
        for u, v in graph.values():
            for x in u:
                for y in v:
                    if (x, y) not in edges and (y, x) not in edges:
                        edges.add((x, y))
        
        persistence = 0
        while nodes or edges:
            if nodes:
                node = random.choice(nodes)
                nodes.remove(node)
                persistence += 1
            elif edges:
                edge = random.choice(list(edges))
                edges.remove(edge)
                persistence += 1
        return persistence

    def size(bp):
        return len(bp)

    n = random.randint(5, 40)
    bp_ip2 = generate_bp(n)
    bp_random = generate_bp(n)

    persistence_ip2 = persistent_homology(state_transition_graph(bp_ip2))
    persistence_random = persistent_homology(state_transition_graph(bp_random))

    metric_name = "persistence"
    metric_value_ip2 = persistence_ip2
    metric_value_random = persistence_random
    instances_tested = 1
    conjecture_holds_ip2 = persistence_ip2 >= n
    conjecture_holds_random = persistence_random <= math.log(size(bp_random))
    counterexample_ip2 = "" if conjecture_holds_ip2 else "IP_2 BP does not show Ω(n) persistence"
    counterexample_random = "" if conjecture_holds_random else "Random BP shows O(log size(P)) behavior"

    return {
        "metric_name": metric_name,
        "metric_value_ip2": metric_value_ip2,
        "metric_value_random": metric_value_random,
        "instances_tested": instances_tested,
        "conjecture_holds_ip2": conjecture_holds_ip2,
        "counterexample_ip2": counterexample_ip2,
        "conjecture_holds_random": conjecture_holds_random,
        "counterexample_random": counterexample_random
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
    support_fraction_ip2 = sum(1 for x in results_ip2 if x >= n) / len(results_ip2)

    mean_random = sum(results_random) / len(results_random)
    std_random = math.sqrt(sum((x - mean_random) ** 2 for x in results_random) / len(results_random))
    support_fraction_random = sum(1 for x in results_random if x <= math.log(size(bp_random))) / len(results_random)

    if support_fraction_ip2 >= 0.8 and support_fraction_random >= 0.8:
        print(f"RESULT: SUPPORTED mean_ip2={mean_ip2} std_ip2={std_ip2} support_fraction_ip2={support_fraction_ip2}")
        print(f"RESULT: SUPPORTED mean_random={mean_random} std_random={std_random} support_fraction_random={support_fraction_random}")
    elif any(x < n for x in results_ip2):
        first_failing_seed = seeds[results_ip2.index(min(results_ip2))]
        print(f"RESULT: FALSIFIED counterexample_ip2='IP_2 BP does not show Ω(n) persistence' first_failing_seed={first_failing_seed}")
    elif any(x > math.log(size(bp_random)) for x in results_random):
        first_failing_seed = seeds[results_random.index(max(results_random))]
        print(f"RESULT: FALSIFIED counterexample_random='Random BP shows O(log size(P)) behavior' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")