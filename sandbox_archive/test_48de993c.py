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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph

    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for node in range(n):
            neighbors = set(graph[node])
            for neighbor in neighbors:
                if neighbor not in neighbors:
                    rank += 1
        return rank

    def minimal_symplectic_volume(graph):
        n = len(graph)
        volume = 0
        for node in graph:
            for neighbor in graph[node]:
                if (node, neighbor) not in edges and (neighbor, node) not in edges:
                    volume += 1
        return volume

    a = 1.0
    d_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in d_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, n)
            if graph is None:
                continue
            r_G = communication_complexity_rank(graph)
            vol_m_G = minimal_symplectic_volume(graph)
            ratio = Fraction(vol_m_G, r_G) if r_G != 0 else Fraction(1, 1)
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)

            threshold = a * math.log2(2)**n
            if ratio < threshold:
                conjecture_holds = False
                counterexample = f"Graph size {n}, ratio {ratio} < threshold {threshold}"

    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    support_fraction = Fraction(instances_tested, len(d_values) * 5)

    return {
        "metric_name": "Ratio of Minimal Symplectic Volume to Communication Complexity Rank",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")