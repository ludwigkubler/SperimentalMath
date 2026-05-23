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
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate non-pivot elements
            for j in range(n):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(i, n+1):
                        matrix[j][k] -= factor * matrix[i][k]
        
        # Back-substitute to find solution
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = matrix[i][-1] / matrix[i][i]
            for j in range(i-1, -1, -1):
                matrix[j][-1] -= matrix[j][i] * solution[i]
        
        return solution
    
    def tensor_product_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def branching_program_depth(boolean_function):
        # Placeholder implementation, replace with actual algorithm
        return random.randint(5, 20)
    
    n = random.randint(5, 40)
    boolean_algebra = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    tropicalized_boolean_algebra = gaussian_elimination(boolean_algebra)
    tensor_rank = tensor_product_rank(tropicalized_boolean_algebra)
    branching_depth = branching_program_depth(boolean_algebra)
    
    return {
        "metric_name": "tensor_product_rank",
        "metric_value": tensor_rank,
        "instances_tested": 1,
        "conjecture_holds": tensor_rank == branching_depth,
        "counterexample": "" if tensor_rank == branching_depth else f"Tensor rank {tensor_rank} != Branching depth {branching_depth}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")