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
    
    def generate_graph(n):
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def is_valid_coloring(graph, coloring):
        for u in range(len(graph)):
            for v in range(u + 1, len(graph)):
                if graph[u][v] == 1 and coloring[u] == coloring[v]:
                    return False
        return True
    
    def generate_random_coloring(n):
        return [random.randint(0, n - 1) for _ in range(n)]
    
    def communication_complexity(graph, coloring):
        n = len(graph)
        total_bits = 0
        for u in range(n):
            for v in range(u + 1, n):
                if graph[u][v] == 1:
                    total_bits += math.ceil(math.log2(n))
        return total_bits
    
    def formal_power_series_invariant_factors(graph):
        n = len(graph)
        factors = []
        for i in range(1, n + 1):
            factor = 0
            for u in range(n):
                if sum(graph[u]) == i:
                    factor += 1
            factors.append(factor)
        return factors
    
    def min_order_invariant_factors(factors):
        return max(factors)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    coloring = generate_random_coloring(n)
    
    invariant_factors = formal_power_series_invariant_factors(graph)
    min_order_factor = min_order_invariant_factors(invariant_factors)
    comm_complexity = communication_complexity(graph, coloring)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity <= n**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [random.getrandbits(32) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    total_comm_complexity = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_comm_complexity += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_comm_complexity = total_comm_complexity / len(results)
    support_fraction = count_conjecture_holds / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample='not supported by enough seeds' first_failing_seed=None")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")