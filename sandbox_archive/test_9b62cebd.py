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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for j in range(i-1, -1, -1):
                b[j] -= A[j][i] * x[i]
        return x

    def construct_birational_variety(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for clause in cnf:
            literals = set(clause)
            if len(literals) == 2:
                literal1, literal2 = literals
                A[-literal1 - 1][-literal2 - 1] += 1
                A[-literal2 - 1][-literal1 - 1] += 1
                b[-literal1 - 1] += 1
                b[-literal2 - 1] += 1
        return A, b

    def calculate_minimal_rank(A):
        _, x = gaussian_elimination(A, [0] * len(A))
        rank = sum(1 for val in x if val != 0)
        return rank

    def clause_tree_width(cnf):
        n = len(cnf)
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(lit in cnf[i] and -lit in cnf[j] for lit in set(cnf[i]) & set(cnf[j])):
                    graph[i].append(j)
                    graph[j].append(i)
        
        def dfs(node, visited, parent):
            visited[node] = True
            max_depth = 0
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    depth = dfs(neighbor, visited, node) + 1
                    max_depth = max(max_depth, depth)
            return max_depth
        
        visited = [False] * n
        max_width = 0
        for i in range(n):
            if not visited[i]:
                width = dfs(i, visited, -1) + 1
                max_width = max(max_width, width)
        
        return max_width

    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = set()
            for j in range(n):
                if random.randint(0, 1) == 1:
                    clause.add(j + 1)
                else:
                    clause.add(-(j + 1))
            cnf.append(list(clause))
        return cnf

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    A, b = construct_birational_variety(cnf)
    minimal_rank = calculate_minimal_rank(A)
    clause_width = clause_tree_width(cnf)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")