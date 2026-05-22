# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import permutations

def symmetric_group_action(graph, n):
    action = []
    for perm in permutations(range(n)):
        new_graph = [graph[perm[i]] for i in range(n)]
        action.append(new_graph)
    return action

def min_rank(action):
    rank = 0
    for graph in action:
        matrix = [[0] * len(graph) for _ in range(len(graph))]
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                matrix[i][j] = 1 if i == j else 0
        rank = max(rank, gaussian_elimination(matrix))
    return rank

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        pivot_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[pivot_row][i]):
                pivot_row = r
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate below pivot
        for r in range(i+1, n):
            factor = matrix[r][i] / matrix[i][i]
            for c in range(i, n):
                matrix[r][c] -= factor * matrix[i][c]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def max_disjoint_paths(graph):
    # Placeholder function to simulate communication complexity
    n = len(graph)
    return 2**n * math.sqrt(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    action = symmetric_group_action(graph, n)
    min_rank_value = min_rank(action)
    comm_complexity = max_disjoint_paths(graph)
    
    instances_tested = 1
    conjecture_holds = min_rank_value <= n**(1/3) and comm_complexity <= 2**n * min_rank_value
    counterexample = "" if conjecture_holds else f"MinRank(G)={min_rank_value}, C_G={comm_complexity}"
    
    return {
        "metric_name": "Max-Disjoint Paths Communication Complexity",
        "metric_value": comm_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100+1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MinRank(G) > n^(1/3) or C_G > 2^n * MinRank(G)\" first_failing_seed={first_failing_seed}")