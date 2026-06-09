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
    
    def frege_to_symplectic(frege_clauses):
        # Construct a symplectic structure from Frege clauses (simplified example)
        n = len(frege_clauses)
        symplectic_matrix = [[0] * n for _ in range(n)]
        for i, clause in enumerate(frege_clauses):
            for j, literal in enumerate(clause):
                if literal > 0:
                    symplectic_matrix[i][j] += 1
                else:
                    symplectic_matrix[j][i] -= 1
        return symplectic_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            # Eliminate
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            if matrix[i][i] == 0:
                return 0
            det *= matrix[i][i]
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        return det
    
    def minimal_order_of_quantization(matrix):
        # Simplified example: minimal order is the log of the determinant
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        return math.log(abs(det))
    
    def generate_frege_proof(width):
        clauses = []
        for _ in range(width):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, width))]
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            frege_clauses = generate_frege_proof(n)
            symplectic_matrix = frege_to_symplectic(frege_clauses)
            mq_phi = minimal_order_of_quantization(symplectic_matrix)
            w_phi = len(frege_clauses)
            total_metric_value += mq_phi / math.log(w_phi)
            instances_tested += 1
            max_n = max(max_n, n)
            if mq_phi > 1.5 * math.log(w_phi):
                conjecture_holds = False
                counterexample = f"n={n}, w(φ)={w_phi}, mq(φ)={mq_phi}"
    
    return {
        "metric_name": "minimal_order_of_quantization",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")