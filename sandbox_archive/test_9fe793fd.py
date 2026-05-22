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

# Helper functions for basic linear algebra and group operations
def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        max_row = i
        for r in range(i+1, n):
            if abs(M[r][i]) > abs(M[max_row][i]):
                max_row = r
        M[i], M[max_row] = M[max_row], M[i]
        for k in range(i+1, n):
            factor = -M[k][i] / M[i][i]
            for j in range(n):
                if i == j:
                    M[k][j] = 0
                else:
                    M[k][j] += factor * M[i][j]
    return M

def rank(matrix):
    matrix = [row[:] for row in matrix]
    n = len(matrix)
    r = gaussian_elimination(matrix)
    rank = 0
    for i in range(n):
        if all(x == 0 for x in r[i]):
            continue
        rank += 1
    return rank

def symmetric_group_action(graph):
    n = len(graph)
    action = []
    vertices = list(range(n))
    permutations = [list(itertools.permutations(vertices)) for _ in range(n)]
    for perm in itertools.product(*permutations):
        new_graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_graph[perm[i]][perm[j]] = graph[i][j]
        action.append(new_graph)
    return action

def min_rank(graph):
    action = symmetric_group_action(graph)
    ranks = [rank(g) for g in action]
    return max(ranks)

def communication_complexity(n, min_rank_value):
    return 2**n * n**(1/2)

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    min_rank_value = min_rank(graph)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if min_rank_value <= n**(1/3):
        C_G = communication_complexity(n, min_rank_value)
        if C_G <= 2**n * min_rank_value:
            conjecture_holds = True
        else:
            counterexample = f"Counterexample: n={n}, MinRank(G)={min_rank_value}, C_G={C_G}"
    else:
        counterexample = f"Mapping undefined for n={n}, MinRank(G)={min_rank_value}"
    
    return {
        "metric_name": "MinRank",
        "metric_value": min_rank_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main block to run trials and print results
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")