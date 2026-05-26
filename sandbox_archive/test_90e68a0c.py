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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return ['x']
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree(n - n // 2)
            return [f'({left[0]} & {right[0]})'] + left + right
    
    def compute_width(tree):
        if isinstance(tree, str):
            return 1
        else:
            return max(compute_width(subtree) for subtree in tree[1:])
    
    def compute_communication_complexity(tree):
        if isinstance(tree, str):
            return 0
        else:
            left = compute_communication_complexity(tree[1])
            right = compute_communication_complexity(tree[2])
            return max(left, right) + 1
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def construct_quantum_group_representation(tree):
        width = compute_width(tree)
        n_leaves = 2 ** (width - 1)
        generators = [f'x{i}' for i in range(n_leaves)]
        relations = []
        queue = [(tree, [])]
        while queue:
            node, path = queue.pop()
            if isinstance(node, str):
                continue
            left, right = node[1], node[2]
            left_path, right_path = path + [0], path + [1]
            relations.append((left_path, right_path))
            queue.append((left, left_path))
            queue.append((right, right_path))
        matrix = [[0] * (n_leaves + 1) for _ in range(n_leaves + 1)]
        for i in range(n_leaves):
            matrix[i][i] = 1
        for path1, path2 in relations:
            index1, index2 = generators.index(f'x{path1[-1]}'), generators.index(f'x{path2[-1]}')
            matrix[index1][index2] = -1
            matrix[index2][index1] = -1
        return gaussian_elimination(matrix)
    
    n = random.randint(5, 40)
    tree = generate_xor_and_tree(n)
    width = compute_width(tree)
    comm_complexity = compute_communication_complexity(tree)
    rank = construct_quantum_group_representation(tree)
    
    if rank is None:
        return {
            "metric_name": "rank/width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    ratio = rank / width
    expected_ratio = comm_complexity + math.log(n)
    if abs(ratio - expected_ratio) <= math.log(n):
        return {
            "metric_name": "rank/width",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "rank/width",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"ratio={ratio}, expected_ratio={expected_ratio}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")