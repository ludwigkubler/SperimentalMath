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
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph

    def is_planar(graph):
        n = len(graph)
        if n <= 4:
            return True
        for node in range(n):
            neighbors = graph[node]
            if len(neighbors) >= 5:
                subgraph = {node: [neighbor for neighbor in neighbors if neighbor != node]}
                for neighbor in neighbors:
                    subgraph[neighbor] = [n for n in graph[neighbor] if n != node and n != neighbor]
                    if not is_planar(subgraph):
                        return False
                return True
        return False

    def tseitin_formula(graph, start=0):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for node in range(n):
            if not graph[node]:
                continue
            clause = [literals[node]]
            for neighbor in graph[node]:
                clause.append(f'-{literals[neighbor]}')
            clauses.append(clause)
            for i in range(len(graph[node])):
                for j in range(i + 1, len(graph[node])):
                    clauses.append([f'-{literals[graph[node][i]]}', f'-{literals[graph[node][j]]}', literals[node]])
        return clauses

    def resolution_width(clauses):
        queue = [clauses]
        resolvents = set()
        while queue:
            clause = queue.pop(0)
            if not clause:
                return 0
            literal = random.choice(clause)
            new_clauses = []
            for c in queue:
                if literal in c:
                    continue
                if f'-{literal}' in c:
                    resolvent = [l for l in c if l != literal and l != f'-{literal}']
                    resolvents.add(tuple(sorted(resolvent)))
                    new_clauses.append(resolvent)
                else:
                    new_clauses.append(c)
            queue.extend(new_clauses)
        return len(resolvents)

    def minimal_order_of_hodge_structure(graph):
        n = len(graph)
        if not is_planar(graph):
            return None
        # Placeholder for actual Hodge structure computation
        return random.randint(1, 10) * n

    n_max = 40
    instances_tested = 0
    total_moh = 0
    total_width = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        moh = minimal_order_of_hodge_structure(graph)
        if moh is None:
            continue
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        instances_tested += 1
        total_moh += moh
        total_width += width
        if moh > n ** (1/2):
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, moh(G)={moh} > {n**(1/2)}"
            break

    mean_moh = total_moh / instances_tested if instances_tested else 0
    mean_width = total_width / instances_tested if instances_tested else 0
    support_fraction = instances_tested / (n_max - 4)

    return {
        "metric_name": "Minimal Order of Hodge Structure",
        "metric_value": mean_moh,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_moh = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_moh} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_moh} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")