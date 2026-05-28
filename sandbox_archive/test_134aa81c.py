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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges
    
    def adjacency_matrix(edges, n):
        mat = [[0] * n for _ in range(n)]
        for u, v in edges:
            mat[u][v] = 1
            mat[v][u] = 1
        return mat
    
    def gaussian_elimination(mat):
        m, n = len(mat), len(mat[0])
        rank = 0
        for i in range(n):
            if rank < m:
                pivot_row = rank
                while pivot_row < m and mat[pivot_row][i] == 0:
                    pivot_row += 1
                if pivot_row == m:
                    continue
                mat[rank], mat[pivot_row] = mat[pivot_row], mat[rank]
                for j in range(n):
                    if i != j:
                        factor = -mat[j][i] / mat[rank][i]
                        for k in range(n):
                            mat[j][k] += factor * mat[rank][k]
            rank += 1
        return rank
    
    def noncrossed_product_algebra_rank(adj_matrix):
        n = len(adj_matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        result = [identity]
        for _ in range(2, n + 1):
            next_result = []
            for mat in result:
                new_mat = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            new_mat[i][j] += mat[i][k] * adj_matrix[k][l] * mat[l][j]
                next_result.append(new_mat)
            result.extend(next_result)
        return len(result) - 1
    
    def bp_width(adj_matrix):
        n = len(adj_matrix)
        visited = [False] * n
        stack = []
        width = 0
        
        def dfs(node, level):
            nonlocal width
            if visited[node]:
                return
            visited[node] = True
            stack.append((node, level))
            for neighbor in range(n):
                if adj_matrix[node][neighbor] == 1 and not visited[neighbor]:
                    dfs(neighbor, level + 1)
            while stack[-1][0] == node:
                stack.pop()
                width = max(width, len(stack))
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return width
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    adj_matrix = adjacency_matrix(edges, n)
    
    rank = noncrossed_product_algebra_rank(adj_matrix)
    bp_width_val = bp_width(adj_matrix)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if rank <= 3 * bp_width_val:
        conjecture_holds = True
    
    return {
        "metric_name": "rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
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
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"seed {first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")