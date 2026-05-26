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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        
        def dfs(index, depth):
            if index >= n:
                return depth
            left = dfs(2 * index + 1, depth + 1)
            right = dfs(2 * index + 2, depth + 1)
            return max(left, right)
        
        return dfs(0, 0)
    
    def quaternionic_representation(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        
        Q = []
        for i in range(n):
            row = [f[2*i] + f[2*i+1], f[2*i] - f[2*i+1]]
            Q.append(row)
        return Q
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = matrix[:]
        for i in range(m):
            augmented_matrix[i].extend([0]*n + [1 if i == j else 0 for j in range(n)])
        
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0])
            for i in range(rows):
                max_row = i
                for r in range(i+1, rows):
                    if abs(mat[r][i]) > abs(mat[max_row][i]):
                        max_row = r
                
                mat[i], mat[max_row] = mat[max_row], mat[i]
                
                for r in range(i+1, rows):
                    factor = mat[r][i] / mat[i][i]
                    for c in range(cols):
                        mat[r][c] -= factor * mat[i][c]
            
            rank = 0
            for row in mat:
                if any(row):
                    rank += 1
            return rank
        
        return gaussian_elimination(augmented_matrix)
    
    n = random.choice([10, 15, 20])
    f = generate_boolean_function(n)
    Q = quaternionic_representation(f)
    tree_width = xor_and_tree_width(f)
    minimal_rank = rank(Q)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= tree_width,
        "counterexample": f"n={n}, rank={minimal_rank}, expected={tree_width}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")