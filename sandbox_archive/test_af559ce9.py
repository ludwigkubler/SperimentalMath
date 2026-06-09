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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges or (v, u) in edges:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
                break
        return graph

    def resolution_width(graph):
        n = len(graph)
        if n == 1:
            return 0
        queue = []
        for u in range(n):
            if len(graph[u]) == 1:
                queue.append(u)
        width = 0
        while queue:
            next_queue = set()
            for u in queue:
                for v in graph[u]:
                    graph[v].remove(u)
                    if len(graph[v]) == 1:
                        next_queue.add(v)
            queue = next_queue
            width += 1
        return width

    def count_generators(graph):
        n = len(graph)
        generators = set()
        visited = [False] * n
        for u in range(n):
            if not visited[u]:
                stack = [u]
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        generators.add(node)
                        for neighbor in graph[node]:
                            stack.append(neighbor)
        return len(generators)

    n_values = [5, 10, 15, 20, 30, 40]
    total_g = 0
    total_w = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, d=3)
            if graph is None:
                continue
            w = resolution_width(graph)
            g = count_generators(graph)
            total_g += g
            total_w += w
            instances_tested += 1

    mean_g = total_g / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(g * w for g, w in zip([mean_g] * instances_tested, [mean_w] * instances_tested)) - 
                               sum(g) * sum(w)) / math.sqrt((instances_tested * sum(g**2 for g in [mean_g] * instances_tested) - sum(g)**2) *
                                                          (instances_tested * sum(w**2 for w in [mean_w] * instances_tested) - sum(w)**2))
    mean_abs_diff = abs(mean_g - mean_w)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9 and mean_abs_diff <= 5,
        "counterexample": "" if correlation_coefficient >= 0.9 and mean_abs_diff <= 5 else f"correlation_coefficient={correlation_coefficient}, mean_abs_diff={mean_abs_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")