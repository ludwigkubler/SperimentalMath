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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i+1}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = []
            for j in range(d):
                clause.append(literals[graph[i][j]])
            clauses.append(clause)
            for j in range(i + 1, n):
                for k in range(d):
                    for l in range(k + 1, d):
                        clauses.append([f'~{literals[graph[i][k]]}', f'~{literals[graph[j][l]]}'])
        return literals, clauses
    
    def resolution_width(clauses):
        queue = [clause[:] for clause in clauses]
        learned_clauses = []
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(lit == f'~{other}' for lit in queue[i] for other in queue[j]):
                        common_lit = next(lit for lit in queue[i] if lit.startswith('~') and any(other.startswith(lit[1:]) for other in queue[j]))
                        new_clause = [lit for lit in queue[i] if lit != common_lit and not lit.startswith('~')]
                        new_clause.extend([lit for lit in queue[j] if lit != common_lit[-1:] and not lit.startswith('~')])
                        learned_clauses.append(new_clause)
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(learned_clauses) + 1
            queue.append(new_clause)
    
    def minimal_order(graph):
        n = len(graph)
        d = len(graph[0])
        order = 0
        for i in range(n):
            for j in range(i + 1, n):
                if len(set(graph[i]) & set(graph[j])) == 2:
                    order += 1
        return order
    
    n = random.randint(5, 40)
    d = random.randint(3, min(2 * (n - 1), n))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "invalid_d_regular_graph"
        }
    
    literals, clauses = tseitin_formula(graph)
    width = resolution_width(clauses)
    order = minimal_order(graph)
    
    return {
        "metric_name": "min_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")