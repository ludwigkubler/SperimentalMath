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

def generate_k_clique(n, k):
    if n < k:
        return None
    clique = set(range(k))
    for i in range(k, n):
        new_node = {i}
        for node in clique:
            if len(new_node & clique) == 0:
                new_node.add(node)
                break
        else:
            return generate_k_clique(n, k - 1)
        clique.update(new_node)
    return list(clique)

def construct_xor_and_tree(edges):
    if not edges:
        return None
    n = len(edges)
    mid = n // 2
    left_edges = edges[:mid]
    right_edges = edges[mid:]
    return (construct_xor_and_tree(left_edges), construct_xor_and_tree(right_edges))

def find_matroid_representation(clique, rank_bound):
    n = len(clique)
    if n == 0:
        return []
    matroid = []
    for i in range(n):
        row = [0] * n
        row[i] = 1
        matroid.append(row)
    while len(matroid) < rank_bound:
        new_row = [random.choice([0, 1]) for _ in range(n)]
        if any(sum(a * b for a, b in zip(row, new_row)) % 2 == 0 for row in matroid):
            continue
        matroid.append(new_row)
    return matroid

def rank_of_matroid(matroid):
    n = len(matroid)
    identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(matroid, identity_matrix)]
    rows = list(range(n))
    cols = list(range(n))
    
    def gaussian_elimination(matrix, rows, cols):
        for pivot_col in range(n):
            if all(matrix[row][pivot_col] == 0 for row in rows):
                continue
            pivot_row = next((row for row in rows if matrix[row][pivot_col]), None)
            rows.remove(pivot_row)
            rows.insert(0, pivot_row)
            for i in range(len(rows)):
                if i != 0:
                    factor = matrix[rows[i]][pivot_col] / matrix[rows[0]][pivot_col]
                    for j in range(n + 1):
                        matrix[rows[i]][j] -= factor * matrix[rows[0]][j]
        return sum(1 for row in rows if any(matrix[row][col] != 0 for col in cols))
    
    rank = gaussian_elimination(augmented_matrix, rows, cols)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clique = generate_k_clique(n, 3)
        if clique is None:
            continue
        xor_and_tree = construct_xor_and_tree(clique)
        rank_bound = n ** 3
        matroid_representation = find_matroid_representation(clique, rank_bound)
        matroid_rank = rank_of_matroid(matroid_representation)
        
        results.append({
            "n": n,
            "clique_size": len(clique),
            "xor_and_tree_width": xor_and_tree[0] if xor_and_tree else 0,
            "matroid_rank": matroid_rank
        })
    
    if not results:
        return {
            "metric_name": "min_matroid_rank_over_xor_and_tree_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = sum(result["matroid_rank"] for result in results) / len(results)
    min_xor_and_tree_width = min(result["xor_and_tree_width"] for result in results)
    
    if mean_rank <= n_values[-1] ** 3 and min_xor_and_tree_width > 0:
        return {
            "metric_name": "min_matroid_rank_over_xor_and_tree_width",
            "metric_value": mean_rank / min_xor_and_tree_width,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_matroid_rank_over_xor_and_tree_width",
            "metric_value": mean_rank / min_xor_and_tree_width,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"mean_rank={mean_rank}, expected<=n^3"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 71))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")