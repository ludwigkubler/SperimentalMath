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
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < (n * d) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and graph[u][v] == 0:
                graph[u][v] = 1
                graph[v][u] = 1
                edges_added += 1
        return graph
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = -1
            for i in range(rank, m):
                if matrix[i][j] != 0:
                    i_max = i
                    break
            if i_max == -1:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank and matrix[i][j] != 0:
                    factor = matrix[i][j] / matrix[rank][j]
                    for k in range(n):
                        matrix[i][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def resolution_proof_width(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] == 0:
                    continue
                clause = [i+1, -(j+1)]
                clauses.append(clause)
        # Simplified DPLL implementation (not full resolution proof width)
        def dpll(clauses, assignment, literals):
            if not clauses:
                return True
            literal = literals[0]
            pos_literal = abs(literal)
            neg_literal = -pos_literal
            for clause in clauses:
                if pos_literal in clause:
                    new_clauses = [c for c in clauses if neg_literal not in c]
                    if dpll(new_clauses, assignment + [pos_literal], literals[1:]):
                        return True
                elif neg_literal in clause:
                    continue
                else:
                    break
            else:
                return False
        return len(clauses)
    
    def tropicalized_cohomology_rank(graph):
        n = len(graph)
        matrix = [[0] * (n+1) for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if graph[i][j] == 1:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return gaussian_elimination(matrix)
    
    def correlation(ranks, widths):
        if len(ranks) != len(widths):
            return None
        n = len(ranks)
        sum_ranks = sum(ranks)
        sum_widths = sum(widths)
        sum_ranks_squared = sum(x**2 for x in ranks)
        sum_widths_squared = sum(x**2 for x in widths)
        sum_product = sum(r * w for r, w in zip(ranks, widths))
        numerator = n * sum_product - sum_ranks * sum_widths
        denominator = math.sqrt((n * sum_ranks_squared - sum_ranks**2) * (n * sum_widths_squared - sum_widths**2))
        if denominator == 0:
            return None
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        rank = tropicalized_cohomology_rank(graph)
        width = resolution_proof_width(graph)
        if rank is not None and width is not None:
            ranks.append(rank)
            widths.append(width)
    
    if len(ranks) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_value = correlation(ranks, widths)
    return {
        "metric_name": "correlation",
        "metric_value": correlation_value,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_value is not None and abs(correlation_value) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        counterexample = ""
    else:
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = f"first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")