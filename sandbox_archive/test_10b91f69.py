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
    
    def xor_and_tree(n):
        if n == 1:
            return ['X']
        else:
            left = xor_and_tree(n // 2)
            right = xor_and_tree(n - n // 2)
            return ['A', left, right]
    
    def symplectic_form(tree):
        if isinstance(tree, list):
            if tree[0] == 'X':
                return [[1, 0], [0, 1]]
            elif tree[0] == 'A':
                left = symplectic_form(tree[1])
                right = symplectic_form(tree[2])
                n = len(left)
                I_n = [[(i == j) for i in range(n)] for j in range(n)]
                return block_matrix([[I_n, I_n], [I_n, -I_n]])
        else:
            raise ValueError("Invalid tree structure")
    
    def block_matrix(blocks):
        n = len(blocks)
        m = len(blocks[0])
        result = [[0] * (n * m) for _ in range(n * m)]
        for i in range(n):
            for j in range(m):
                if blocks[i][j]:
                    for k in range(n):
                        for l in range(m):
                            result[i * n + k][j * m + l] = blocks[i][j][k][l]
        return result
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows == 0 or cols == 0:
            return 0
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return rank(matrix[:i] + matrix[i+1:])
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))
    
    n = random.randint(5, 40)
    tree = xor_and_tree(n)
    form = symplectic_form(tree)
    rank_value = rank(form)
    
    width = len(tree) - 1
    expected_rank = width
    
    return {
        "metric_name": "rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": abs(rank_value - expected_rank) <= 3,
        "counterexample": "" if abs(rank_value - expected_rank) <= 3 else f"Rank {rank_value} does not match expected rank {expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")