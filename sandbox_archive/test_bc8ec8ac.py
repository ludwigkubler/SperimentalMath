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
        graph = [[] for _ in range(n)]
        degree_sum = n * d
        if degree_sum % 2 != 0:
            return None
        edges = degree_sum // 2
        added_edges = set()
        while len(added_edges) < edges:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or (u, v) in added_edges or (v, u) in added_edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            added_edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = set()
        for clause in clauses:
            queue.add(tuple(sorted(clause)))
        resolvents = []
        while queue:
            u, v = random.sample(queue, 2)
            common_lit = next((lit for lit in u if lit.startswith('-') and -int(lit[1:]) in v), None)
            if common_lit is not None:
                new_clause = [x for x in u if x != common_lit] + [x for x in v if x != '-'+common_lit]
                new_clause.sort()
                resolvents.append(tuple(new_clause))
                queue.add(tuple(new_clause))
        return len(resolvents)
    
    def algebraic_k_theory_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    u = stack.pop()
                    if not visited[u]:
                        visited[u] = True
                        for v in graph[u]:
                            if not visited[v]:
                                stack.append(v)
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 3))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        rank = algebraic_k_theory_rank(graph)
        results.append((width, rank))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    widths = [r[0] for r in results]
    ranks = [r[1] for r in results]
    mean_width = sum(widths) / len(widths)
    mean_rank = sum(ranks) / len(ranks)
    std_width = math.sqrt(sum((w - mean_width) ** 2 for w in widths) / len(widths))
    std_rank = math.sqrt(sum((r - mean_rank) ** 2 for r in ranks) / len(ranks))
    
    correlation_coefficient = sum((widths[i] - mean_width) * (ranks[i] - mean_rank) for i in range(len(results))) / (len(results) * std_width * std_rank)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(w <= 3 * r for w, r in results),
        "counterexample": "" if correlation_coefficient >= 0.7 and all(w <= 3 * r for w, r in results) else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")