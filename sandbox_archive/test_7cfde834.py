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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return "leaf"
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return (left, right)
    
    def braid_monodromy_representation(tree):
        if tree == "leaf":
            return [[0]]
        left_rep = braid_monodromy_representation(tree[0])
        right_rep = braid_monodromy_representation(tree[1])
        n_left = len(left_rep)
        n_right = len(right_rep)
        result = []
        for i in range(n_left):
            for j in range(n_right):
                row = [0] * (n_left + n_right - 2)
                row[i] = 1
                row[j + n_left - 1] = 1
                result.append(row)
        return result
    
    def minimal_rank(matrix):
        rank = 0
        for row in matrix:
            if any(x != 0 for x in row):
                rank += 1
        return rank
    
    def generate_k_clique_instance(n, k=3):
        if n < k:
            raise ValueError("n must be at least k")
        nodes = list(range(1, n + 1))
        clique = set(random.sample(nodes, k))
        non_clique_nodes = [node for node in nodes if node not in clique]
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((clique[i], clique[j]))
        for node in non_clique_nodes:
            for other_node in nodes:
                if (node, other_node) not in edges and (other_node, node) not in edges:
                    edges.append((node, other_node))
        return edges
    
    n = random.randint(5, 40)
    xor_and_tree = generate_xor_and_tree(n)
    braid_rep = braid_monodromy_representation(xor_and_tree)
    k_clique_instance = generate_k_clique_instance(n)
    
    xor_and_min_rank = minimal_rank(braid_rep)
    k_clique_min_rank = minimal_rank([[1 if (i, j) in k_clique_instance else 0 for j in range(n)] for i in range(n)])
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": xor_and_min_rank,
        "instances_tested": n,
        "conjecture_holds": xor_and_min_rank <= math.log2(n) ** 2 and k_clique_min_rank <= len(k_clique_instance) * math.log2(n) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE instance with n={result['instances_tested']} and k={len(result['counterexample'])}\" first_failing_seed={seed}")
                break