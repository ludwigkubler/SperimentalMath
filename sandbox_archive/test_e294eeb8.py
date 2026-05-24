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
    
    def generate_bp(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
        return bp
    
    def construct_quadratic_form(bp):
        n = len(bp)
        Q = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                if bp[i] == bp[j]:
                    Q[i][j] = 1
                    Q[j][i] = 1
        
        return Q
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        
        return det
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        
        return rank
    
    def bp_size(bp):
        return sum(bp)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_bp(n)
        Q = construct_quadratic_form(bp)
        rank = min_rank(Q)
        size = bp_size(bp)
        
        if rank == 0 or size == 0:
            continue
        
        results.append({
            "n": n,
            "rank": rank,
            "size": size
        })
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank_values = [result["rank"] for result in results]
    size_values = [result["size"] for result in results]
    
    mean_rank = sum(min_rank_values) / len(min_rank_values)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in min_rank_values) / len(min_rank_values))
    
    conjecture_holds = all(1.5 * math.log(size, 2) <= rank for rank, size in zip(min_rank_values, size_values))
    counterexample = "" if conjecture_holds else f"BP of size {size_values[0]} with rank {min_rank_values[0]}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(min_rank_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results if result["instances_tested"] > 0) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")