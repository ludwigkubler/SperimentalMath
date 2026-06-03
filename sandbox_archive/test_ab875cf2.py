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
    
    def generate_tseitin_formula(n, d):
        if n % d != 0 or n < 2 * d + 1:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(d):
            for j in range(i+1, d+1):
                edges.append((vertices[i], vertices[j]))
        formula = []
        for v in vertices:
            clause = [v]
            for u in vertices:
                if (u, v) not in edges and (v, u) not in edges:
                    clause.append(-u)
            formula.append(clause)
        return formula

    def gaussian_elimination(A):
        n = len(A)
        m = len(A[0])
        rank = 0
        for i in range(n):
            if rank == m:
                break
            pivot_row = i
            while pivot_row < n and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == n:
                continue
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(m):
                A[i][j] /= A[i][i]
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(m):
                        A[k][j] -= factor * A[i][j]
            rank += 1
        return rank

    def resolution_width(clauses):
        queue = clauses[:]
        seen = set()
        width = 0
        while queue:
            clause = queue.pop(0)
            if any(abs(lit) in seen for lit in clause):
                continue
            new_clauses = []
            for other_clause in queue:
                for lit1 in clause:
                    for lit2 in other_clause:
                        if abs(lit1) == abs(lit2):
                            if lit1 != lit2:
                                new_clauses.append([l for l in other_clause if l != lit2] + [l for l in clause if l != lit1])
            queue.extend(new_clauses)
            seen.update(abs(lit) for lit in clause)
            width = max(width, len(seen))
        return width

    def generate_d_regular_graph(n, d):
        if n % d != 0 or n < 2 * d + 1:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(d):
            for j in range(i+1, d+1):
                edges.append((vertices[i], vertices[j]))
        graph = {v: [] for v in vertices}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        return graph

    def minimal_rank(graph):
        n = len(graph)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = 1
            for j in graph[i]:
                A[i][j] = -1
        return gaussian_elimination(A)

    def resolution_width_from_formula(formula):
        clauses = formula[:]
        return resolution_width(clauses)

    n_max = 40
    instances_tested = 0
    min_ranks = []
    widths = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_d_regular_graph(n, n // 2)
            if graph is None:
                continue
            formula = generate_tseitin_formula(n, n // 2)
            if formula is None:
                continue
            instances_tested += 1
            min_ranks.append(minimal_rank(graph))
            widths.append(resolution_width_from_formula(formula))

    if len(min_ranks) < 30:
        return {
            "metric_name": "minimal_rank",
            "metric_value": sum(min_ranks) / len(min_ranks),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_widths = sum(widths) / len(widths)
    correlation_coefficient = 0
    for i in range(len(min_ranks)):
        correlation_coefficient += (min_ranks[i] - mean_min_ranks) * (widths[i] - mean_widths)
    correlation_coefficient /= math.sqrt(sum((x - mean_min_ranks) ** 2 for x in min_ranks)) * math.sqrt(sum((y - mean_widths) ** 2 for y in widths))

    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_min_ranks,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_min_ranks = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_ranks} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_ranks} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{0.95}\" first_failing_seed={first_failing_seed}")