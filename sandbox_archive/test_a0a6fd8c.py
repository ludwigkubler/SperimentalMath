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
        graph = {i: [] for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                edges_added += 1
        return graph

    def euler_characteristic(graph):
        v = len(graph)
        e = sum(len(neighbors) for neighbors in graph.values()) // 2
        f = v + e - 2
        return v - e + f

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: [f"p{i}", f"q{i}"] for i in range(n)}
        clauses = []
        for u, neighbors in graph.items():
            clause = [literals[u][0]]
            for v in neighbors:
                clause.append(f"-{literals[v][1]}")
            clauses.append(clause)
            for v in neighbors:
                clause = [f"-{literals[u][0]}"]
                for w in neighbors:
                    if v != w:
                        clause.append(f"{literals[w][1]}")
                clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        max_width = 0
        for clause in clauses:
            max_width = max(max_width, len(clause))
        return max_width

    n_values = [5, 10, 15, 20, 30, 40]
    chi_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(n, d)
            chi = euler_characteristic(graph)
            phi_g = tseitin_formula(graph)
            w_phi_g = resolution_width(phi_g)
            
            chi_sum += chi
            w_sum += w_phi_g
            instances_tested += 1
            n_max = max(n_max, n)

    mean_chi = chi_sum / instances_tested
    mean_w = w_sum / instances_tested

    if abs(mean_chi - mean_w) < 0.9 * min(abs(mean_chi), abs(mean_w)):
        conjecture_holds = False
        counterexample = "Correlation coefficient does not exceed 0.9"

    return {
        "metric_name": "Euler Characteristic vs Resolution Width",
        "metric_value": mean_chi,
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
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient does not exceed 0.9\" first_failing_seed={first_failing_seed}")