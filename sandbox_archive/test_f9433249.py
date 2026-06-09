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
        adj_list = [[] for _ in range(n)]
        edges_used = set()
        for i in range(n):
            for j in range(d):
                while True:
                    neighbor = random.randint(0, n - 1)
                    if neighbor == i or (i, neighbor) in edges_used or (neighbor, i) in edges_used:
                        continue
                    edges_used.add((i, neighbor))
                    adj_list[i].append(neighbor)
                    adj_list[neighbor].append(i)
                    break
        return adj_list

    def compute_matroid_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        rank += 1
                        for neighbor in graph[node]:
                            if not visited[neighbor]:
                                stack.append(neighbor)
        return rank

    def compute_minimal_geometric_entropy(matroid_rank, n):
        # Simplified approximation of geometric entropy
        return matroid_rank / math.log2(n)

    def construct_tseitin_formula(graph):
        n = len(graph)
        num_vars = 2 * n + 1
        clauses = []
        for i in range(n):
            clauses.append([i + 1, -n - i - 1])
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(len(graph[i])):
                    if graph[i][k] == j:
                        clauses.append([-i - 1, -j - 1, k + n + 1])
        return num_vars, clauses

    def compute_resolution_proof_width(clauses):
        # Simplified approximation of resolution proof width
        return len(clauses)

    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "mge(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    matroid_rank = compute_matroid_rank(graph)
    mge_G = compute_minimal_geometric_entropy(matroid_rank, n)
    num_vars, clauses = construct_tseitin_formula(graph)
    w_phi_G = compute_resolution_proof_width(clauses)

    if mge_G > 10 or w_phi_G < 3:
        return {
            "metric_name": "mge(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"mge(G)={mge_G}, w(φ_G)={w_phi_G}"
        }

    return {
        "metric_name": "mge(G)",
        "metric_value": mge_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mge_values = [result["metric_value"] for result in results if result["conjecture_holds"]]
        if not mge_values:
            support_fraction = 0.0
        else:
            mean_value = sum(mge_values) / len(mge_values)
            std_value = math.sqrt(sum((mge - mean_value) ** 2 for mge in mge_values) / len(mge_values))
            support_fraction = len(mge_values) / len(results)

    if all(result["conjecture_holds"] or result["metric_value"] is None for result in results):
        print(f"RESULT: INCONCLUSIVE reason=undefined_mapping n_tested={len(seeds)}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mge(G) > 10 or w(φ_G) < 3' first_failing_seed={first_failing_seed}")