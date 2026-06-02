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
    
    def generate_random_code(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def transpose(matrix):
        return [list(row) for row in zip(*matrix)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(matrix, augmented=False):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            if augmented:
                matrix[n][i] /= pivot
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                    if augmented:
                        matrix[n][j] -= factor * matrix[n][i]
        return matrix
    
    def minimal_p_adic_rank(code):
        n = len(code)
        A = code + transpose(code)
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank, n)):
                continue
            rank += 1
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(2 * n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def communication_complexity_rank(code):
        n = len(code)
        min_ranks = []
        for i in range(n):
            row_sum = sum(code[i])
            col_sum = sum(row[i] for row in code)
            min_ranks.append(min(row_sum, col_sum))
        return max(min_ranks)
    
    instances_tested = 0
    n_max = 0
    total_rank = 0
    total_communication_rank = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            code = generate_random_code(n)
            min_rank = minimal_p_adic_rank(code)
            communication_rank = communication_complexity_rank(code)
            
            total_rank += min_rank
            total_communication_rank += communication_rank
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = (total_rank * total_communication_rank - instances_tested * total_rank * total_communication_rank / instances_tested) / math.sqrt((total_rank ** 2 - instances_tested * total_rank ** 2 / instances_tested) * (total_communication_rank ** 2 - instances_tested * total_communication_rank ** 2 / instances_tested))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if not r["conjecture_holds"]) >= 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")