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
    n = random.randint(5, 40)
    k = random.randint(1, min(n-1, 10))
    
    # Generate a random XOR-AND tree with n leaves
    def generate_xor_and_tree(n):
        if n == 1:
            return [0]
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return [left, right]
    
    tree = generate_xor_and_tree(n)
    
    # Compute the braid monodromy representation for XOR-AND trees
    def xor_and_braid_monodromy(tree):
        if isinstance(tree, int):
            return [[1]]
        left = xor_and_braid_monodromy(tree[0])
        right = xor_and_braid_monodromy(tree[1])
        result = []
        for l in left:
            for r in right:
                result.append([l[i] + r[i] for i in range(len(l))])
        return result
    
    braid_rep = xor_and_braid_monodromy(tree)
    
    # Compute the minimal rank of the braid monodromy representation
    def matrix_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows == 0 or cols == 0:
            return 0
        
        # Gaussian elimination to find the rank
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                continue
            
            for j in range(i+1, rows):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    minimal_rank = matrix_rank(braid_rep)
    
    # Check the conjecture
    expected_minimal_rank = math.log2(n) ** 2
    conjecture_holds = abs(minimal_rank - expected_minimal_rank) / expected_minimal_rank <= 0.1
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, expected_minimal_rank={expected_minimal_rank:.2f}, actual_minimal_rank={minimal_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")