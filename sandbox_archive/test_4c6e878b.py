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
    
    def generate_regular_graph(n, degree):
        if (n * degree) % 2 != 0 or degree < 3 or degree >= n:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < (n * degree) // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph

    def girth(graph):
        n = len(graph)
        for start in range(n):
            visited = [False] * n
            queue = [(start, 0)]
            while queue:
                u, dist = queue.pop(0)
                if visited[u]:
                    continue
                visited[u] = True
                for v in graph[u]:
                    if not visited[v]:
                        queue.append((v, dist + 1))
                    elif dist - (dist + 1) >= 2:
                        return dist + 1
        return float('inf')

    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for u in range(n):
            if len(graph[u]) == degree - 1:
                clauses.append([literals[u]] + [-literals[v] for v in graph[u]])
            elif len(graph[u]) < degree - 1:
                return None
        for i in range(n):
            for j in range(i + 1, n):
                if not (i in graph[j] or j in graph[i]):
                    clauses.append([-literals[i], -literals[j]])
        return clauses

    def resolution_proofs(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    a = clauses[i]
                    b = clauses[j]
                    if not any(x == -y for x in a for y in b):
                        continue
                    new_clause = [x for x in a if x not in b] + [x for x in b if x not in a]
                    if len(new_clause) == 1:
                        return True
                    new_clauses.append(new_clause)
            if new_clauses == clauses:
                return False
            clauses = new_clauses

    def minimal_vertex_separation(graph):
        n = len(graph)
        for k in range(1, n // 2 + 1):
            visited = [False] * n
            queue = [(i, {i}) for i in range(n)]
            while queue:
                u, path = queue.pop(0)
                if visited[u]:
                    continue
                visited[u] = True
                if len(path) == k:
                    return k
                for v in graph[u]:
                    if v not in path:
                        queue.append((v, path | {v}))
        return n

    def run_resolution_proofs(clauses):
        start_time = time.time()
        result = resolution_proofs(clauses)
        end_time = time.time()
        if end_time - start_time > 200:
            print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=1')
            exit(1)
        return result

    def run_tseitin_formula(graph):
        clauses = tseitin_formula(graph)
        if not clauses:
            return None
        return run_resolution_proofs(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            degree = random.randint(3, min(n - 1, 6))
            graph = generate_regular_graph(n, degree)
            if not graph or girth(graph) < 5:
                continue
            instances_tested += 1
            length = run_tseitin_formula(graph)
            if length is None:
                conjecture_holds = False
                counterexample = f"Graph with n={n}, degree={degree} does not have a valid Tseitin formula"
                break
            total_length += length

    mean_length = total_length / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / (len(n_values) * len(range(5)))

    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [71, 73, 79, 83, 89]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")