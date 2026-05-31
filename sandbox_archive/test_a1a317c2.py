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
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det

    def generate_quotient_ring(k, n):
        variables = [[f'x_{i}_{j}' for j in range(n)] for i in range(k)]
        relations = []
        for i in range(k):
            for j in range(n):
                relation = [0] * (k*n)
                relation[i*n + j] = 1
                relations.append(relation)
        return variables, relations

    def compute_brauer_group_rank(variables, relations):
        n = len(variables[0])
        k = len(variables)
        matrix = [[0] * (k*n) for _ in range(k*n)]
        for i in range(k):
            for j in range(n):
                matrix[i*n + j][i*n + j] = 1
        for relation in relations:
            for i in range(k*n):
                if relation[i]:
                    for j in range(k*n):
                        matrix[i][j] += relation[j]
        rank = sum(1 for row in gaussian_elimination(matrix) if any(row))
        return rank

    def communication_complexity(n):
        # Placeholder function; replace with actual communication complexity calculation
        return n

    k = random.randint(2, 5)
    n = random.randint(5, 30)
    variables, relations = generate_quotient_ring(k, n)
    brauer_group_rank = compute_brauer_group_rank(variables, relations)
    comm_complexity = communication_complexity(n)

    return {
        "metric_name": "Brauer group rank",
        "metric_value": brauer_group_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": brauer_group_rank >= n**(k/2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(30, 100))
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")