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
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            factor = Fraction(matrix[i][i])
            for j in range(i + 1, n):
                matrix[j][i] /= factor
        
        # Back substitution
        result = [0] * n
        for i in range(n - 1, -1, -1):
            result[i] = matrix[i][-1]
            for j in range(i + 1, n):
                result[i] -= matrix[i][j] * result[j]
            result[i] /= Fraction(matrix[i][i])
        
        return result
    
    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for c in range(len(matrix)):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * matrix[0][c] * sub_det
        return det
    
    def construct_quadratic_form(bp):
        n = len(bp)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if bp[i] == 1 and bp[j] == 1:
                    A[i][j] += 1
                    A[j][i] += 1
        return A
    
    def min_rank(matrix):
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    bp = [random.choice([0, 1]) for _ in range(n)]
    
    quadratic_form = construct_quadratic_form(bp)
    min_rank_val = min_rank(quadratic_form)
    
    size_bp = len(bp)
    conjecture_holds = (min_rank_val <= 1.5 * math.log2(size_bp)) and (min_rank_val >= n if bp == [0] * n else True)
    counterexample = "" if conjecture_holds else f"BP: {bp}, min_rank: {min_rank_val}, expected: ({math.log2(size_bp)}, {n})"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank_val,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")