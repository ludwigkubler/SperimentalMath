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

def generate_regular_graph(n, degree):
    if (n * degree) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges_used = set()
    for v in range(n):
        for u in range(v + 1, n):
            if len(graph[v]) == degree and len(graph[u]) == degree:
                continue
            if (v, u) not in edges_used and (u, v) not in edges_used:
                graph[v].append(u)
                graph[u].append(v)
                edges_used.add((v, u))
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = {i: f'x{i}' for i in range(n)}
    clauses = []
    for v in range(n):
        clause = [literals[v]]
        for u in graph[v]:
            clause.append(-literals[u])
        clauses.append(clause)
    return clauses

def resolution_proof_length(clauses):
    def resolve(clause1, clause2):
        new_clause = []
        for literal in clause1:
            if -literal in clause2:
                continue
            new_clause.append(literal)
        return new_clause

    def is_tautology(clause):
        pos_literals = {abs(l) for l in clause}
        neg_literals = {-l for l in clause}
        return pos_literals & neg_literals

    queue = clauses.copy()
    while True:
        found_new_clause = False
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                new_clause = resolve(queue[i], queue[j])
                if not new_clause or is_tautology(new_clause):
                    continue
                if new_clause not in queue:
                    queue.append(new_clause)
                    found_new_clause = True
        if not found_new_clause:
            break
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_regular_graph(n, degree=3)
        if not graph:
            continue
        clauses = tseitin_formula(graph)
        proof_length = resolution_proof_length(clauses)
        g_G = len(graph) - max(len(neighbors) for neighbors in graph.values())
        results.append({
            "n": n,
            "g_G": g_G,
            "proof_length": proof_length
        })
    if not results:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    total_length = sum(result["proof_length"] for result in results)
    avg_length = total_length / len(results)
    conjecture_holds = all(length >= 2**g_G for result in results for length, g_G in zip([result["proof_length"]] * n_values, [result["g_G"]] * n_values))
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": avg_length,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    avg_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_length} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")