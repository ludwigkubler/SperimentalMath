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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(i+1, n), d-1)
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges.add((i, j))
        return graph

    def shannon_entropy(graph):
        n = len(graph)
        degree_sum = sum(sum(row) for row in graph)
        p = [sum(row) / (2 * degree_sum) for row in graph]
        entropy = -sum(p_i * math.log2(p_i) if p_i > 0 else 0 for p_i in p)
        return entropy

    def reflection_poset(graph):
        n = len(graph)
        reflections = set()
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] == 1:
                    reflections.add((i, j))
        return reflections

    def isomorphic_subgroup(reflections, automorphisms):
        # Placeholder for actual subgroup isomorphism check
        return True

    n_max = 40
    instances_tested = 0
    total_r = 0.0
    max_r = -1.0
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            instances_tested += 1
            h_G = shannon_entropy(graph)
            R_G = reflection_poset(graph)
            if len(R_G) > 4 * h_G:
                counterexample = f"n={n}, |R(G)|={len(R_G)}, h(G)={h_G}"
                return {
                    "metric_name": "correlation_coefficient",
                    "metric_value": -1.0,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            r = len(R_G) / h_G if h_G > 0 else 0
            total_r += r
            max_r = max(max_r, r)

    correlation_coefficient = total_r / instances_tested

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and max_r <= 4 * h_G,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["correlation_coefficient"] for r in results) >= 0.7:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")