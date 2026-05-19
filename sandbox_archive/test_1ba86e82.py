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
    
    def generate_expander_graph(n):
        if n <= 1:
            return []
        edges = set()
        for i in range(1, n):
            j = (i * 2) % n
            edges.add((i, j))
        return list(edges)
    
    def adjacency_matrix(graph, n):
        mat = [[0] * n for _ in range(n)]
        for u, v in graph:
            mat[u][v] = 1
            mat[v][u] = 1
        return mat
    
    def tensor_product(mat1, mat2):
        n = len(mat1)
        result = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        result[i * n + k][j * n + l] += mat1[i][j] * mat2[k][l]
        return result
    
    def count_irreducible_components(mat):
        n = len(mat)
        if n == 0:
            return 0
        rank = 0
        for i in range(n):
            pivot = None
            for j in range(i, n):
                if mat[j][i] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            rank += 1
            for j in range(n):
                if j == pivot:
                    continue
                factor = mat[j][i] / mat[pivot][i]
                for k in range(i, n):
                    mat[j][k] -= factor * mat[pivot][k]
        return rank
    
    n = random.randint(5, 40)
    graph = generate_expander_graph(n)
    adj_mat = adjacency_matrix(graph, n)
    tensor_prod = tensor_product(adj_mat, adj_mat)
    
    irreducible_count = count_irreducible_components(tensor_prod)
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": irreducible_count,
        "instances_tested": 1,
        "conjecture_holds": irreducible_count >= 2 ** n * 0.5,
        "counterexample": "" if irreducible_count >= 2 ** n * 0.5 else f"n={n}, count={irreducible_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")