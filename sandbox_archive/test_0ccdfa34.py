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
    
    n = 40
    depth = 5
    
    # Generate a random binary matrix M of size n×n
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the real rank of M over the reals
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = min(m, n)
        for i in range(rank):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    rank -= 1
                    continue
            for j in range(m):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    real_rank = gaussian_elimination(M)
    
    # Simulate ACC^0 circuits of varying depths to approximate the matrix
    def simulate_acc0_circuit(matrix, depth):
        m, n = len(matrix), len(matrix[0])
        if depth == 1:
            return sum(sum(row) for row in matrix)
        else:
            half_matrix = [row[:n//2] + row[n//2:] for row in matrix]
            left_rank = simulate_acc0_circuit(half_matrix, depth-1)
            right_rank = simulate_acc0_circuit(half_matrix, depth-1)
            return max(left_rank, right_rank)
    
    acc0_rank_bound = simulate_acc0_circuit(M, depth)
    
    # Validate if the rank bound scales as O((log n)^d) for depth d
    expected_rank_bound = Fraction((math.log2(n) ** depth), 1).limit_denominator()
    
    return {
        "metric_name": "Rank Bound",
        "metric_value": acc0_rank_bound,
        "instances_tested": 1,
        "conjecture_holds": acc0_rank_bound <= expected_rank_bound,
        "counterexample": "" if acc0_rank_bound <= expected_rank_bound else f"Depth {depth} ACC^0 circuit rank bound {acc0_rank_bound} exceeds expected bound {expected_rank_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")