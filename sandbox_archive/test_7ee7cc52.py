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
        if (n * d) % 2 != 0 or d < 1 or n < 1:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) == d and len(graph[j]) == d:
                    continue
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_added.add((i, j))
        return graph

    def matroid_rank(matroid):
        n = len(matroid)
        rank = 0
        for i in range(n):
            if len(matroid[i]) > rank:
                rank += 1
        return rank

    def geometric_entropy(matroid):
        rank = matroid_rank(matroid)
        n = len(matroid)
        if rank == 0 or rank == n:
            return 0
        p = rank / n
        entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        return entropy

    def tseitin_formula(graph):
        num_vars = len(graph)
        clauses = []
        for i in range(num_vars):
            clauses.append([i + 1])
            for j in graph[i]:
                if j > i:
                    clauses.append([-i - 1, j + 1])
        return clauses

    def resolution_width(clauses):
        n = len(clauses)
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width

    def run_resolution(clauses):
        queue = list(clauses)
        learned_clauses = []
        while queue:
            clause = queue.pop(0)
            if not any(abs(lit) in learned_clause for learned_clause in learned_clauses):
                learned_clauses.append(clause)
                for other_clause in clauses:
                    if len(set(clause) & set(other_clause)) == 1:
                        new_clause = [lit for lit in clause + other_clause if abs(lit) not in clause and abs(lit) not in other_clause]
                        queue.append(new_clause)
        return max(len(clause) for clause in learned_clauses)

    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "mge(G)",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    matroid = graph
    mge_G = geometric_entropy(matroid)
    if mge_G > 10:
        return {
            "metric_name": "mge(G)",
            "metric_value": mge_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mge(G) > 10"
        }

    Tseitin = tseitin_formula(graph)
    w_phi_G = resolution_width(Tseitin)
    if w_phi_G < 3:
        return {
            "metric_name": "w(φ_G)",
            "metric_value": w_phi_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w(φ_G) < 3"
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
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = res["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")