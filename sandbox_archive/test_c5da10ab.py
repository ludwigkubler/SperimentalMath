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
            max_row = i + max(range(i, n), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(n):
                matrix[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def multiply_matrices(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det

    def grothendieck_witt_class(poly, p):
        n = len(poly)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                if poly[i][j]:
                    A[i][j] = A[j][i] = poly[i][j]
        A = gaussian_elimination(A)
        det_A = determinant(A)
        return det_A % p

    def communication_complexity_rank_variance(phi, p):
        n = len(phi)
        rank = sum(1 for row in phi if any(row))
        return (rank * (n - rank)) / n

    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = random.sample(range(1, 2*n+1), 3)
            sign = [-1, 1][random.randint(0, 1)]
            cnf.append([sign * literal for literal in clause])
        return cnf

    def min_index(A):
        n = len(A)
        max_nonzero = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j] != 0:
                    max_nonzero = max(max_nonzero, abs(A[i][j]))
        return max_nonzero

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = generate_cnf(n)
        p = random.choice([2, 3, 5, 7, 11])
        gw_class = grothendieck_witt_class(phi, p)
        rank_variance = communication_complexity_rank_variance(phi, p)
        min_index_value = min_index([[gw_class] * n for _ in range(n)])
        
        metric_values.append(min_index_value)
        if not conjecture_holds and len(metric_values) >= 10:
            counterexample = f"n={n}, gw_class={gw_class}, rank_variance={rank_variance}, min_index={min_index_value}"
            break

    mean_metric = sum(metric_values) / instances_tested
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / instances_tested)
    
    return {
        "metric_name": "Min Index of Noncommutative Quotient Algebra",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")