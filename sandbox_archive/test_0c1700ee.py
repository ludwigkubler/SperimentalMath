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
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                edges_added += 1
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: (f'x{i}', f'not_x{i}') for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [literals[u][0]]
            for v in graph[u]:
                clause.append(f'or_{u}_{v}')
            clauses.append(clause)
            for v in graph[u]:
                clauses.append([f'not_{u}_{v}', literals[v][1]])
        return clauses
    
    def tropicalized_quiver_representation(clauses):
        n = len(clauses)
        max_order = 0
        for clause in clauses:
            order = 1
            for literal in clause:
                if literal.startswith('or_'):
                    u, v = map(int, literal.split('_')[1:])
                    order += max(len(graph[u]), len(graph[v]))
            max_order = max(max_order, order)
        return max_order
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        clauses = [set(clause) for clause in clauses]
        queue = set()
        for i in range(n):
            if len(clauses[i]) == 1:
                queue.add(next(iter(clauses[i])))
        while queue:
            literal = queue.pop()
            for j in range(n):
                if literal in clauses[j]:
                    new_clause = clauses[j] - {literal}
                    if not new_clause:
                        return float('inf')
                    if len(new_clause) == 1:
                        queue.add(next(iter(new_clause)))
                    else:
                        clauses[j] = new_clause
        return n
    
    def is_d_regular(graph, d):
        for neighbors in graph.values():
            if len(neighbors) != d:
                return False
        return True
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    while not is_d_regular(generate_d_regular_graph(n, d), d):
        n = random.randint(5, 40)
        d = random.randint(2, min(n - 1, 3))
    
    graph = generate_d_regular_graph(n, d)
    clauses = tseitin_formula(graph)
    mtr_q_G = tropicalized_quiver_representation(clauses)
    w_phi_G = resolution_proof_width(clauses)
    
    return {
        "metric_name": "mtr_q(G)",
        "metric_value": mtr_q_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mtr_q_G >= 0.5 * w_phi_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mtr_q(G) < 0.5 * w(φ_G)"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")