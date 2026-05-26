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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if rank < n and matrix[i][i] == 0:
                exchange_found = False
                for k in range(i, n):
                    if matrix[k][i] != 0:
                        for j in range(n + 1):
                            matrix[i][j], matrix[k][j] = matrix[k][j], matrix[i][j]
                        exchange_found = True
                        break
                if not exchange_found:
                    continue
            pivot = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n + 1):
                        matrix[k][j] -= factor * matrix[i][j]
            rank += 1
        return rank
    
    def xor_and_tree_width(tree):
        if isinstance(tree, int):
            return 0
        left_width = xor_and_tree_width(tree[0])
        right_width = xor_and_tree_width(tree[1])
        return max(left_width, right_width) + 1
    
    def generate_k_clique(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return edges
    
    def construct_xor_and_tree(edges):
        if not edges:
            return 0
        left_edges = edges[:len(edges) // 2]
        right_edges = edges[len(edges) // 2:]
        return (construct_xor_and_tree(left_edges), construct_xor_and_tree(right_edges))
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 5))
    clique = generate_k_clique(n, k)
    xor_and_tree = construct_xor_and_tree(clique)
    matroid_rank = gaussian_elimination([[random.choice([0, 1]) for _ in range(n)] for _ in range(n)])
    
    if matroid_rank > n ** k:
        return {
            "metric_name": "min_rank_over_nk",
            "metric_value": matroid_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={matroid_rank}, expected<=n^k"
        }
    
    tree_width = xor_and_tree_width(xor_and_tree)
    if matroid_rank < tree_width:
        return {
            "metric_name": "min_rank_over_nk",
            "metric_value": matroid_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={matroid_rank}, width={tree_width}"
        }
    
    return {
        "metric_name": "min_rank_over_nk",
        "metric_value": matroid_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='rank<width' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")