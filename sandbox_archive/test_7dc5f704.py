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
    
    def generate_and_or_tree(depth, branching_factor):
        if depth == 1:
            return random.choice(['0', '1'])
        else:
            children = [generate_and_or_tree(random.randint(1, depth-1), branching_factor) for _ in range(branching_factor)]
            return f'({", ".join(children)})'
    
    def tropicalize(tree):
        if tree == '0':
            return [[0]]
        elif tree == '1':
            return [[math.inf]]
        else:
            children = [tropicalize(child) for child in tree[1:-1].split(',')]
            result = []
            for i in range(len(children)):
                for j in range(len(children[i])):
                    new_row = [child[j] + 1 if child == children[i][j] else math.inf for child in children]
                    result.append(new_row)
            return result
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [i] for i, row in enumerate(matrix)]
        for col in range(n):
            max_row = max(range(col, m), key=lambda r: abs(augmented_matrix[r][col]))
            augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
            if augmented_matrix[col][col] == 0:
                continue
            denom = augmented_matrix[col][col]
            for i in range(col, n + 1):
                augmented_matrix[col][i] /= denom
            for i in range(m):
                if i != col:
                    factor = augmented_matrix[i][col]
                    for j in range(col, n + 1):
                        augmented_matrix[i][j] -= factor * augmented_matrix[col][j]
        return sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(n)))
    
    depths = [2, 5, 10, 15, 20, 30, 40]
    branching_factors = [2, 5, 10, 15, 20]
    results = []
    
    for depth in depths:
        for _ in range(5):
            tree = generate_and_or_tree(depth, random.choice(branching_factors))
            lie_algebra = tropicalize(tree)
            rank_value = rank(lie_algebra)
            results.append((depth, branching_factor, rank_value))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_depth = sum(depth for depth, _, _ in results)
    total_branching_factor = sum(branching_factor for _, branching_factor, _ in results)
    total_rank = sum(rank_value for _, _, rank_value in results)
    mean_depth = total_depth / len(results)
    mean_branching_factor = total_branching_factor / len(results)
    mean_rank = total_rank / len(results)
    
    expected_rank = (mean_depth ** 1.5) * (mean_branching_factor ** 0.5)
    if abs(mean_rank - expected_rank) > 0.1 * expected_rank:
        return {
            "metric_name": "minimal_rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"rank={mean_rank}, expected={expected_rank}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank deviation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")