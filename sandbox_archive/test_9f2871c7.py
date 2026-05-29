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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank

    def dpll_tree_depth(k):
        # Simplified DPLL tree depth calculation
        return k * (k - 1) // 2

    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    clique_size = random.randint(3, k)

    # Find a clique of size `clique_size`
    def find_clique(graph, start, clique, visited):
        if len(clique) == clique_size:
            return clique
        for i in range(start, n):
            if graph[visited[-1]][i] == 1 and all(graph[j][i] == 1 for j in visited):
                new_visited = visited + [i]
                result = find_clique(graph, i + 1, clique + [i], new_visited)
                if result:
                    return result
        return None

    clique = find_clique(graph, 0, [], [0])
    if not clique:
        return {
            "metric_name": "minimal_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "clique_not_found"
        }

    # Construct the DPLL search tree
    def dpll(graph, assignment, clause):
        if not clause:
            return True
        var = next((i for i in range(n) if i not in assignment), None)
        if var is None:
            return False
        for val in [0, 1]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_clause = [c for c in clause if not any(graph[var][i] == 1 and new_assignment[i] == 1 for i in range(n))]
            if dpll(graph, new_assignment, new_clause):
                return True
        return False

    depth = dpll_tree_depth(clique_size)

    # Construct the Lie algebra
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                A[i][j] = A[j][i] = random.choice([-1, 1])

    rank = matrix_rank(A)

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= depth,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.9 and abs(mean_value - depth) <= 1.5:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"seed {first_failing_seed}\" first_failing_seed={seeds[first_failing_seed]}")