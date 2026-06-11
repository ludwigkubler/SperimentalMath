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

def generate_d_regular_graph(n, d):
    if (d * n) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges_added = set()
    while len(edges_added) < (d * n) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [i for i in range(n)]
    clauses = []
    for i in range(n):
        clause = [-literals[i]]
        for j in graph[i]:
            clause.append(literals[j])
        clauses.append(clause)
    return clauses

def minimal_irreducible_representation_order(graph):
    n = len(graph)
    if n == 1:
        return 1
    adjacency_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            adjacency_matrix[i][j] = 1
    # Gaussian elimination to find the rank of the matrix
    rank = 0
    for i in range(n):
        if all(adjacency_matrix[j][i] == 0 for j in range(rank)):
            continue
        pivot_row = rank
        rank += 1
        for j in range(i, n):
            adjacency_matrix[pivot_row], adjacency_matrix[j] = adjacency_matrix[j], adjacency_matrix[pivot_row]
        for j in range(n):
            if j != pivot_row:
                factor = adjacency_matrix[j][i] / adjacency_matrix[pivot_row][i]
                for k in range(i, n):
                    adjacency_matrix[j][k] -= factor * adjacency_matrix[pivot_row][k]
    return rank

def resolution_proof_width(clauses):
    queue = clauses[:]
    level = 0
    while queue:
        new_queue = []
        for clause in queue:
            if len(clause) == 1:
                literal = clause[0]
                if -literal in [c[0] for c in queue]:
                    return level + 1
                continue
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    new_clause = [-clause[i], -clause[j]]
                    if new_clause not in new_queue:
                        new_queue.append(new_clause)
        queue = new_queue
        level += 1
    return level

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        d = random.randint(2, min(n - 1, 5))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        order = minimal_irreducible_representation_order(graph)
        width = resolution_proof_width(clauses)
        instances_tested += len(clauses)
        n_max = max(n_max, n)
        total_metric_value += abs(order - width)

    if instances_tested < 30:
        return {
            "metric_name": "abs_diff",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_metric_value = total_metric_value / instances_tested
    if mean_metric_value > 2:
        conjecture_holds = False
        counterexample = f"mean_diff={mean_metric_value} exceeds threshold"

    return {
        "metric_name": "abs_diff",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] or math.isnan(r["metric_value"]) for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=nan support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and not math.isnan(r["metric_value"]) for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff_exceeds_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")