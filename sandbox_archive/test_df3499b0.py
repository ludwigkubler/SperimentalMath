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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            if matrix[i][i] == 0:
                return None  # Singular matrix
            for j in range(i + 1, rows):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def branching_program_depth(boolean_function):
        n = len(boolean_function)
        if n == 1:
            return 1
        left_child = boolean_function[:n//2]
        right_child = boolean_function[n//2:]
        return max(branching_program_depth(left_child), branching_program_depth(right_child)) + 1
    
    def tensor_product_rank(boolean_algebra):
        rows, cols = len(boolean_algebra), len(boolean_algebra[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n = random.randint(5, 40)
    boolean_function = generate_boolean_function(n)
    branching_depth = branching_program_depth(boolean_function)
    tensor_rank = tensor_product_rank(gaussian_elimination(boolean_function))
    
    return {
        "metric_name": "Branching Program Depth vs Tensor Product Rank",
        "metric_value": abs(branching_depth - tensor_rank),
        "instances_tested": 1,
        "conjecture_holds": branching_depth == tensor_rank,
        "counterexample": "" if branching_depth == tensor_rank else f"n={n}, BP depth={branching_depth}, Tensor rank={tensor_rank}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(r["metric_value"] > 1 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] > 1)
        print(f"RESULT: FALSIFIED counterexample='depth > rank' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")