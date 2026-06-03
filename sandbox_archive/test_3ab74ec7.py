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
    
    def construct_symplectic_matrix(f):
        n = len(f)
        if n % 2 != 0:
            raise ValueError("Number of input bits must be even")
        m = n // 2
        S = [[0] * (2 * m) for _ in range(2 * m)]
        for i in range(m):
            for j in range(m):
                if f[i + j * m]:
                    S[2 * i][2 * j + 1] = 1
                    S[2 * i + 1][2 * j] = -1
                    S[2 * j][2 * i + 1] = 1
                    S[2 * j + 1][2 * i] = -1
        return S
    
    def communication_complexity(f):
        n = len(f)
        m = n // 2
        cc = 0
        for i in range(m):
            for j in range(m):
                if f[i + j * m]:
                    cc += 1
        return cc
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        augmented_matrix = [row[:] + [0] for row in matrix]
        for i in range(m):
            if augmented_matrix[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            pivot = augmented_matrix[i][i]
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(m):
                if j != i and augmented_matrix[j][i] != 0:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        S = construct_symplectic_matrix(f)
        r = min_rank(S)
        cc = communication_complexity(f)
        min_ranks.append(r)
        comm_complexities.append(cc)
    
    if len(min_ranks) < 30 or len(comm_complexities) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(min_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_cc = sum(comm_complexities) / len(comm_complexities)
    correlation = (sum((min_ranks[i] - mean_rank) * (comm_complexities[i] - mean_cc) for i in range(len(min_ranks)))) / \
                  math.sqrt(sum((min_ranks[i] - mean_rank)**2 for i in range(len(min_ranks)))) / \
                  math.sqrt(sum((comm_complexities[i] - mean_cc)**2 for i in range(len(comm_complexities))))
    max_diff = max(abs(min_ranks[i] - comm_complexities[i]) for i in range(len(min_ranks)))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and max_diff <= 3,
        "counterexample": "" if correlation >= 0.8 and max_diff <= 3 else "Correlation too low or diff too high"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")