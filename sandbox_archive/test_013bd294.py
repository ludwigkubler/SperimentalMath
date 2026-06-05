# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def generate_random_graph(n, d=3):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    edges = set()
    for i in range(d):
        nodes = list(range(n))
        random.shuffle(nodes)
        for j in range(1, d):
            edge = (nodes[0], nodes[j])
            if edge not in edges and edge[::-1] not in edges:
                edges.add(edge)
    return {i: [] for i in range(n)}, edges

def tseitin_formula(graph, n):
    clauses = []
    for node in range(n):
        literals = [f'x{i}' for i in range(node * d + 1, (node + 1) * d)]
        clause = ['~'] + literals
        clauses.append(clause)
        for literal in literals:
            clauses.append([literal])
        for i in range(len(literals)):
            for j in range(i + 1, len(literals)):
                clauses.append(['~', literals[i], '~', literals[j]])
    return clauses

def resolution_width(clauses):
    queue = set()
    for clause in clauses:
        if len(clause) == 1:
            queue.add(clause[0])
        else:
            queue.add(tuple(sorted(clause)))
    while True:
        new_clauses = []
        found_resolvent = False
        for c1, c2 in combinations(queue, 2):
            resolvents = set()
            for l1 in c1:
                if '~' + l1 in c2:
                    resolvents.add(tuple(sorted([x for x in c1 if x != l1] + [x for x in c2 if x != '~' + l1])))
            if not resolvents:
                continue
            found_resolvent = True
            new_clauses.extend(resolvents)
        if not found_resolvent:
            break
        queue.update(new_clauses)
    return max(len(c) for c in queue)

def min_sheaf_order(graph):
    n, _ = graph
    order = 0
    for node in range(n):
        neighbors = graph[node]
        if len(neighbors) > order:
            order = len(neighbors)
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_random_graph(n)
        clauses = tseitin_formula(graph, n)
        sheaf_order = min_sheaf_order(graph)
        width = resolution_width(clauses)
        results.append((sheaf_order, width))
    if not results:
        return {
            "metric_name": "Ratio of Sheaf Order to Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    ratio = sum(s / w for s, w in results) / len(results)
    return {
        "metric_name": "Ratio of Sheaf Order to Resolution Width",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(ratio - n) / n < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE reason=insufficient_data n_tested=<k>")
    else:
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=<y> support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")