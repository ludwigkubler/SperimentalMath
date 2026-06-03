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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_symplectic_matrix(f):
        n = int(math.log2(len(f)))
        m = n
        S = [[0] * (2 * m) for _ in range(2 * m)]
        
        for i in range(n):
            for j in range(m):
                if f[i + j * m]:
                    S[2 * i][2 * j] = 1
                    S[2 * i + 1][2 * j + 1] = 1
                    S[2 * i][2 * j + 1] = -1
                    S[2 * i + 1][2 * j] = -1
        
        return S
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        m = n
        cc = 0
        
        for i in range(n):
            for j in range(m):
                if f[i + j * m]:
                    cc += 1
        
        return cc
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        pivot_col = 0
        
        for i in range(rows):
            while pivot_col < cols and all(matrix[i][j] == 0 for j in range(pivot_col, cols)):
                pivot_col += 1
            
            if pivot_col >= cols:
                break
            
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            for j in range(rows):
                if i != j and matrix[j][pivot_col] != 0:
                    factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[i][k]
            
            pivot_row += 1
            rank += 1
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        S = construct_symplectic_matrix(f)
        cc = communication_complexity(f)
        
        if len(S) != 2 * n or any(len(row) != 2 * n for row in S):
            return {
                "metric_name": "minimal_rank",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": 0,
                "conjecture_holds": False,
                "counterexample": "symplectic_matrix_construction_failed"
            }
        
        rank = gaussian_elimination(S)
        
        min_ranks.append(rank)
        comm_complexities.append(cc)
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_cc = sum(comm_complexities) / len(comm_complexities)
    correlation_coefficient = 0
    mean_abs_diff = 0
    
    if len(min_ranks) > 1 and len(comm_complexities) > 1:
        n_pairs = len(min_ranks) - 1
        numerator = sum((min_ranks[i] - mean_rank) * (comm_complexities[i] - mean_cc) for i in range(n_pairs))
        denominator = math.sqrt(sum((min_ranks[i] - mean_rank)**2 for i in range(n_pairs)) * sum((comm_complexities[i] - mean_cc)**2 for i in range(n_pairs)))
        
        if denominator != 0:
            correlation_coefficient = numerator / denominator
            mean_abs_diff = sum(abs(min_ranks[i] - comm_complexities[i]) for i in range(n_pairs)) / n_pairs
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, rank={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break