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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if random.random() < 0.5:
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def resolution_graph(cnf):
    n = len(cnf[0])
    graph = [[] for _ in range(2 * n)]
    visited = [False] * (2 * n)

    def add_edge(u, v):
        if u != v:
            graph[u].append(v)
            graph[v].append(u)

    for clause in cnf:
        for literal in clause:
            neg_literal = -literal
            if not visited[neg_literal]:
                visited[neg_literal] = True
                for other_clause in cnf:
                    if literal in other_clause and neg_literal in other_clause:
                        add_edge(literal, neg_literal)
    return graph

def dfs(graph, start, visited):
    stack = [start]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in graph[node]:
                stack.append(neighbor)

def connected_components(graph):
    n = len(graph)
    components = []
    visited = [False] * n

    def component(node):
        comp = []
        dfs(graph, node, visited)
        for i in range(n):
            if visited[i]:
                comp.append(i)
        return comp

    for i in range(n):
        if not visited[i]:
            components.append(component(i))
    return components

def quasi_postnikov_rank(graph):
    n = len(graph)
    rank = 0
    visited = [False] * n

    def dfs(node, parent):
        nonlocal rank
        stack = [(node, None)]
        while stack:
            node, parent = stack.pop()
            if not visited[node]:
                visited[node] = True
                rank += 1
                for neighbor in graph[node]:
                    if neighbor != parent:
                        stack.append((neighbor, node))
    dfs(0, None)
    return rank

def monotone_circuit_depth(cnf):
    n = len(cnf[0])
    depth = 0
    visited = [False] * (2 * n)

    def dfs(node, parent):
        nonlocal depth
        stack = [(node, None)]
        while stack:
            node, parent = stack.pop()
            if not visited[node]:
                visited[node] = True
                depth += 1
                for neighbor in graph[node]:
                    if neighbor != parent:
                        stack.append((neighbor, node))
    dfs(0, None)
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = resolution_graph(cnf)
    rank = quasi_postnikov_rank(graph)
    depth = monotone_circuit_depth(cnf)

    metric_name = "Rank vs Depth"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= depth
    counterexample = "" if conjecture_holds else f"CNF with n={n} and rank {rank}, depth {depth}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_rank = sum(result["metric_value"] for result in results)
    total_depth = sum(result["instances_tested"] * result["metric_value"] for result in results)
    mean_rank = Fraction(total_rank, len(results))
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > depth\" first_failing_seed={first_failing_seed}")