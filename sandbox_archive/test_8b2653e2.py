# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(d):
                neighbor = random.randint(0, n - 1)
                while neighbor == i or (i, neighbor) in edges_added or (neighbor, i) in edges_added:
                    neighbor = random.randint(0, n - 1)
                graph[i].append(neighbor)
                graph[neighbor].append(i)
                edges_added.add((i, neighbor))
        return graph
    
    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def find_min_order_hodge_classes(graph):
        n = len(graph)
        hodge_classes = [0] * n
        for i in range(n):
            hodge_classes[i] = sum(1 for _ in graph[i])
        return max(hodge_classes)
    
    def construct_circuit(graph):
        n = len(graph)
        clauses = [[i, j] for i in range(n) for j in range(i + 1, n)]
        assignment = [random.choice([0, 1]) for _ in range(n)]
        satisfiable = True
        for clause in clauses:
            if not (assignment[clause[0]] or assignment[clause[1]]):
                satisfiable = False
                break
        return satisfiable
    
    n_max = 40
    instances_tested = 0
    total_m_h = 0
    total_th = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if not is_connected(graph):
                continue
            m_h = find_min_order_hodge_classes(graph)
            th = construct_circuit(graph)
            if th:
                instances_tested += 1
                total_m_h += m_h
                total_th += th
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No satisfiable circuits found"
        }
    
    mean_m_h = total_m_h / instances_tested
    mean_th = total_th / instances_tested
    correlation_coefficient = (instances_tested * sum(m_h * th for m_h, th in zip([mean_m_h] * instances_tested, [mean_th] * instances_tested)) - 
                               sum(m_h) * sum(th)) / (instances_tested * sum((m_h - mean_m_h) ** 2 for m_h in [mean_m_h] * instances_tested) * 
                                                     sum((th - mean_th) ** 2 for th in [mean_th] * instances_tested))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break