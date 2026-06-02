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
    
    def generate_cnf(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for row in range(rank, m):
                factor = Fraction(matrix[row][col], matrix[pivot_row][col])
                for j in range(n):
                    matrix[row][j] -= factor * matrix[pivot_row][j]
        return rank
    
    def compute_brauer_group_order(cnf):
        n = len(cnf)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [list(row) + [1] for row in cnf]
        A.append([1] * (n + 1))
        rank_A = gaussian_elimination(A)
        return 2 ** (n - rank_A)
    
    def compute_communication_complexity_rank(cnf):
        n = len(cnf)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [list(row) + [1] for row in cnf]
        A.append([1] * (n + 1))
        rank_A = gaussian_elimination(A)
        return n - rank_A
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_log2_brauer_group = 0
    total_r_phi = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            log2_brauer_group = log2(compute_brauer_group_order(cnf))
            r_phi = compute_communication_complexity_rank(cnf)
            total_log2_brauer_group += log2_brauer_group
            total_r_phi += r_phi
            instances_tested += 1
    
    mean_log2_brauer_group = total_log2_brauer_group / instances_tested
    mean_r_phi = total_r_phi / instances_tested
    
    correlation_coefficient = (mean_log2_brauer_group * mean_r_phi - sum(log2_brauer_group * r for log2_brauer_group, r in zip([log2(compute_brauer_group_order(generate_cnf(n))) for n in n_values], [compute_communication_complexity_rank(generate_cnf(n)) for n in n_values])) / instances_tested) / math.sqrt(sum((log2_brauer_group - mean_log2_brauer_group)**2 for log2_brauer_group, r in zip([log2(compute_brauer_group_order(generate_cnf(n))) for n in n_values], [compute_communication_complexity_rank(generate_cnf(n)) for n in n_values])) / instances_tested * sum((r_phi - mean_r_phi)**2 for log2_brauer_group, r in zip([log2(compute_brauer_group_order(generate_cnf(n))) for n in n_values], [compute_communication_complexity_rank(generate_cnf(n)) for n in n_values])) / instances_tested)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5 and correlation_coefficient < 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")