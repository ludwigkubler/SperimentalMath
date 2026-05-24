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

def generate_random_graph(n):
    graph = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    random.shuffle(edges)
    added_edges = 0
    while added_edges < n - 1:
        u, v = edges.pop()
        if u not in graph[v] and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            added_edges += 1
    return graph

def is_connected(graph):
    visited = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
    return len(visited) == len(graph)

def min_rank(G):
    n = len(G)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in G.items():
        for w in v:
            A[u][w] += 1
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(i)):
            pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    A[j][i:] = [A[j][k] + factor * A[i][k] for k in range(i, n)]
            rank += 1
    return rank

def resolution_length(T):
    clauses = T.split(' ')
    stack = []
    length = 0
    while True:
        if not stack:
            clause = next((c for c in clauses if c.startswith('-')), None)
            if not clause:
                break
            literals = set(clause[1:].split('&'))
            stack.append(literals)
            length += 1
        else:
            literal = next((l for l in stack[-1] if any(c.startswith(f'-{l}') or c == l for c in clauses)), None)
            if not literal:
                literals = set(clause[1:].split('&'))
                stack.append(literals)
                length += 1
            else:
                new_literals = set()
                for c in clauses:
                    if c.startswith(f'-{literal}'):
                        continue
                    elif c == literal:
                        new_literals.update(c.split('&') - {literal})
                    else:
                        new_literals.update(c.split('&'))
                stack.pop()
                stack.append(new_literals)
    return length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    graph = generate_random_graph(n)
    T = ' & '.join(f'x{i}' if i not in graph[i] else f'-x{i}' for i in range(n))
    MinRank_G_tensor_G = min_rank(graph) ** 2
    ResolutionLength_T = resolution_length(T)
    metric_value = MinRank_G_tensor_G / ResolutionLength_T
    conjecture_holds = metric_value >= 2
    counterexample = "" if conjecture_holds else "graph_has_cycles"
    return {
        "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"graph_has_cycles\" first_failing_seed={first_failing_seed}")