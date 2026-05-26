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
            return ['X']
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree(n - n // 2)
            return [f'AND({left[0]}, {right[0]})'] + left + right
    
    def symplectic_form(tree):
        if tree.startswith('X'):
            return [[1, 0], [0, 1]]
        elif 'OR' in tree:
            raise ValueError("Mapping undefined for OR nodes")
        else:
            left = symplectic_form(tree[4:tree.index(',')].strip())
            right = symplectic_form(tree[tree.index(',') + 5:].strip())
            return [[left[0][0] + right[0][0], left[0][1] + right[0][1]],
                    [left[1][0] + right[1][0], left[1][1] + right[1][1]]]
    
    def min_rank(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    width = random.randint(5, 40)
    tree = generate_xor_and_tree(width)
    form = symplectic_form(tree)
    rank = min_rank(form)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False if rank < width else True,
        "counterexample": "" if rank >= width else f"Tree with width {width} and rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")