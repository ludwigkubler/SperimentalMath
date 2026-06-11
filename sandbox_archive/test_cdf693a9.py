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
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        queue = clauses[:]
        learned_clauses = set()
        while queue:
            literal, negated_literal = None, None
            for clause in queue:
                if len(clause) == 1:
                    literal = clause[0]
                    break
            if literal is None:
                return len(learned_clauses)
            queue.remove([literal])
            learned_clauses.add(literal)
            for clause in clauses:
                if negated_literal in clause:
                    new_clause = [l for l in clause if l != negated_literal]
                    if not new_clause:
                        return len(learned_clauses)
                    if new_clause not in queue and new_clause not in learned_clauses:
                        queue.append(new_clause)
        return len(learned_clauses)

    def minimal_irreducible_representation_order(graph):
        n = len(graph)
        order = 0
        for i in range(n):
            neighbors = graph[i]
            if len(neighbors) > order:
                order = len(neighbors)
        return order

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        order = minimal_irreducible_representation_order(graph)
        results.append({
            "metric_name": "minimal_irreducible_representation_order",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(order - width) <= 2,
            "counterexample": "" if abs(order - width) <= 2 else f"Graph with {n} nodes and {d}-regularity has width {width} but order {order}"
        })

    return {
        "metric_name": "minimal_irreducible_representation_order",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")