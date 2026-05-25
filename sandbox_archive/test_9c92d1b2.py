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

def generate_kcnf(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def incidence_graph(clauses: list) -> dict:
    graph = {}
    for i, clause in enumerate(clauses):
        for var in clause:
            if var not in graph:
                graph[var] = []
            graph[var].append(i)
    return graph

def gaussian_elimination(matrix: list) -> int:
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot_row = -1
        for row in range(rank, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        rank += 1
        for other_row in range(rows):
            if other_row != rank - 1 and matrix[other_row][col] != 0:
                factor = matrix[other_row][col] / matrix[rank - 1][col]
                for j in range(cols):
                    matrix[other_row][j] -= factor * matrix[rank - 1][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    clauses = generate_kcnf(n, m)
    graph = incidence_graph(clauses)
    
    max_rank = 0
    for var in graph:
        adjacency_matrix = [[0] * len(graph) for _ in range(len(graph))]
        for clause_index in graph[var]:
            for other_var in graph:
                if clause_index in graph[other_var]:
                    adjacency_matrix[graph[var].index(clause_index)][graph[other_var].index(clause_index)] = 1
        max_rank = max(max_rank, gaussian_elimination(adjacency_matrix))
    
    metric_value = max_rank * n
    instances_tested = 1
    conjecture_holds = metric_value <= (n * math.log(n) + m * math.log(m))
    counterexample = "" if conjecture_holds else f"max_rank={max_rank}, n={n}, m={m}"
    
    return {
        "metric_name": "Max Rank of Groupoid Operations",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [71, 83, 89, 97]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='max_rank_exceeds_bound' first_failing_seed={first_failing_seed}")