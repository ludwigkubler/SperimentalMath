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
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        graph = [[] for _ in range(n)]
        degree_counts = [0] * n
        for i in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.choice([j for j in range(n) if j != u and len(graph[j]) < d])
            graph[u].append(v)
            graph[v].append(u)
            degree_counts[u] += 1
            degree_counts[v] += 1
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"p{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f"~{literals[j]}")
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = list(clauses)
        learned_clauses = set()
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    clause_i = queue[i]
                    clause_j = queue[j]
                    common_literals = [lit for lit in clause_i if lit.startswith("~") and lit[1:] in clause_j]
                    if common_literals:
                        new_clause = [lit for lit in clause_i if not lit.startswith("~") and lit[1:] not in clause_j] + \
                                      [lit for lit in clause_j if not lit.startswith("~") and lit[1:] not in clause_i]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            queue.append(new_clause)
    
    def noncommutative_crossed_product_order(graph):
        n = len(graph)
        order = 0
        for i in range(n):
            for j in graph[i]:
                if i < j and (i, j) not in learned_clauses:
                    learned_clauses.add((i, j))
                    order += 1
        return order
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    orders = []
    widths = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if not graph:
            continue
        phi = tseitin_formula(graph)
        width = resolution_width(phi)
        order = noncommutative_crossed_product_order(graph)
        orders.append(order)
        widths.append(width)
    
    if len(orders) < 30 or len(widths) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = pearson_correlation(orders, widths)
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(orders),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.5 and all(c >= -0.5 for c in [correlation]),
        "counterexample": "" if correlation > 0.5 else f"correlation={correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std={std_corr:.2f} support_fraction={support_fraction:.2f}")
    elif any(r["counterexample"] == "not_enough_instances" for r in results):
        print("RESULT: INCONCLUSIVE not_enough_instances")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")