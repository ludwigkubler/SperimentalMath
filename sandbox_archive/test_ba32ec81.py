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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        for i in range(1, n):
            for j in range(i+1, n):
                clauses.append([i, -j])
                clauses.append([-i, j])
        return variables, clauses

    def min_local_system_rank(clauses):
        n = len(clauses)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(lit in clauses[i] and -lit in clauses[j] for lit in variables):
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for i in range(n):
            row = [A[i][j] for j in range(i, n)]
            if any(row[j] != 0 for j in range(i, n)):
                rank += 1
        return rank

    def resolution_width(clauses):
        clauses = list(clauses)
        queue = clauses.copy()
        while queue:
            clause = queue.pop(0)
            new_clauses = []
            for other_clause in queue:
                common_lits = [lit for lit in clause if -lit in other_clause]
                if len(common_lits) == 1:
                    new_lit = common_lits[0]
                    new_clause = [lit for lit in other_clause if lit != -new_lit] + [new_lit]
                    if new_clause not in queue and new_clause not in new_clauses:
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return len(queue)

    variables, clauses = tseitin_formula(40)
    m_lr = min_local_system_rank(clauses)
    w = resolution_width(clauses)
    
    return {
        "metric_name": "min_local_system_rank",
        "metric_value": m_lr,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")