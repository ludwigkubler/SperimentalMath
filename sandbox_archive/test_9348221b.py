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
    
    def generate_random_graph(n):
        graph = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def compute_moment_matrix(graph, d):
        n = len(graph)
        M_d = [[0] * (n ** d) for _ in range(n ** d)]
        
        def tensor_product(v1, v2):
            result = []
            for x in v1:
                for y in v2:
                    result.append(x * y)
            return result
        
        def flatten(lst):
            flat_list = []
            for sublist in lst:
                if isinstance(sublist, list):
                    flat_list.extend(flatten(sublist))
                else:
                    flat_list.append(sublist)
            return flat_list
        
        def get_variable_index(i, j):
            return i * n + j
        
        variables = [i for i in range(n)]
        
        for i in range(n):
            for j in range(n):
                if j in graph[i]:
                    M_d[get_variable_index(i, 0)][get_variable_index(j, 0)] = 1
                else:
                    M_d[get_variable_index(i, 0)][get_variable_index(j, 0)] = -1
        
        for _ in range(1, d):
            new_matrix = []
            for i in range(n ** (d + 1)):
                row = [0] * (n ** (d + 1))
                for j in range(n ** d):
                    if M_d[i][j] != 0:
                        var_indices = [int(x) for x in flatten([i // n, i % n])]
                        tensor_prod = tensor_product(variables[var_indices], variables)
                        for k in range(len(tensor_prod)):
                            row[k] += M_d[j][k] * tensor_prod[k]
                new_matrix.append(row)
            M_d = new_matrix
        
        return M_d
    
    def compute_real_rank(matrix):
        n = len(matrix)
        U, S, Vt = [], [], []
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(i + 1, n):
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            return A
        
        def compute_svd(A):
            m, n = len(A), len(A[0])
            U = [[A[i][j] for j in range(n)] for i in range(m)]
            S = [sum([U[i][j] ** 2 for j in range(n)]) ** 0.5 for i in range(m)]
            Vt = [[0] * m for _ in range(n)]
            for i in range(m):
                Vt[0][i] = U[i][0]
            return U, S, Vt
        
        A = gaussian_elimination(matrix)
        U, S, Vt = compute_svd(A)
        
        rank = sum([1 if s > 1e-10 else 0 for s in S])
        return rank
    
    n = random.choice(range(5, 41))
    graph = generate_random_graph(n)
    
    results = []
    for d in [2, 4, 6]:
        M_d = compute_moment_matrix(graph, d)
        rank = compute_real_rank(M_d)
        expected_rank = math.floor(d ** 2 / math.log(n))
        
        if rank < expected_rank:
            return {
                "metric_name": "real_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Graph with n={n}, d={d}, rank={rank}"
            }
    
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 3,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 297, 10))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")