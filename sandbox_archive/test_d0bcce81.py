# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(depth):
        if depth == 1:
            return random.choice([0, 1])
        else:
            left = generate_boolean_function(depth - 1)
            right = generate_boolean_function(depth - 1)
            return random.choice([left and right, left or right, not left, not right])
    
    def tropicalized_permutation_pattern(boolean_function):
        n = len(boolean_function)
        pattern = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if boolean_function[i] > boolean_function[j]:
                    pattern[i][j] = 1
                elif boolean_function[i] < boolean_function[j]:
                    pattern[j][i] = 1
        return pattern
    
    def ac0_circuit_depth(boolean_function):
        n = len(boolean_function)
        depth = [0] * n
        for i in range(n):
            if boolean_function[i] == 0:
                depth[i] = 1 + max(depth[j] for j in range(i) if boolean_function[j] == 1)
            else:
                depth[i] = 1 + max(depth[j] for j in range(i) if boolean_function[j] == 0)
        return max(depth)
    
    def matrix_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(m):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    boolean_function = [generate_boolean_function(random.randint(1, 4)) for _ in range(n)]
    pattern = tropicalized_permutation_pattern(boolean_function)
    depth = ac0_circuit_depth(boolean_function)
    rank = matrix_rank(pattern)
    
    ratio = Fraction(rank, depth**2)
    conjecture_holds = ratio <= Fraction(1, 1)  # Placeholder constant C
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 1"
    
    return {
        "metric_name": "Rank/Depth^2",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")