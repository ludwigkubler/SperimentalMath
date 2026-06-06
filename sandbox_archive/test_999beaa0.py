# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_representation(cnf):
        n = len(cnf[0])
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    M[var_index][n] += 1
                else:
                    M[n][var_index] += 1
        return M
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def variance(ranks):
        mean = sum(ranks) / len(ranks)
        return sum((x - mean) ** 2 for x in ranks) / len(ranks)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        M = matrix_representation(cnf)
        rank_value = rank(M)
        if rank_value == float('inf'):
            continue
        results.append(rank_value)
    
    if not results:
        return {
            "metric_name": "Variance of Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid matrix representation found"
        }
    
    var = variance(results)
    return {
        "metric_name": "Variance of Rank",
        "metric_value": var,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": var <= math.log(max(n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(v is not None for v in results):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r <= math.log(max(n_values))) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE some results are None")